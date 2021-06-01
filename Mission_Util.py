import base64
import datetime
import os
import subprocess
import sys
import time

import serial
from reedsolo import ReedSolomonError

import CCSDS_Parameters as ccsds_params
import Mission_Parameters as mission_params
from CCSDS_Decoder import CCSDS_Decoder
from CCSDS_Encoder import CCSDS_Encoder


# Sample process to run in place of Mission telecommand in testing mode
def sample_mission_command_process():
    i = 0
    max_val = 50000

    while i < max_val:
        print(i)
        i += 1


# Sample process to run in place of Mission telecommand in testing mode
def sample_downlink_process():
    i = 0
    max_val = 200000
    print("start")
    while i < max_val:
        i += 1
        if i % 1000 == 0:
            print(i)
    print("done")


# Process to handle mission telecommand
def process_send_mission_telecommand(mission_object, pipe, ttnc_serial_port):

    # Setup serial object to reach ttnc transceiver
    def setup_serial(port):
        ttnc_ser = serial.Serial(port)
        ttnc_ser.baudrate = 9600
        ttnc_ser.timeout = 10
        return ttnc_ser

    # Create CCSDS Encoder
    encoder = CCSDS_Encoder()

    # Create CCSDS Mission telecommand
    mission_start_time = mission_object.mission_datetime.strftime("%d-%m-%Y-%H-%M-%S")
    downlink_start_time = mission_object.downlink_datetime.strftime("%d-%m-%Y-%H-%M-%S")
    ccsds_mission_telecommand = encoder.generate_mission_telecommand(
        ccsds_params.TELECOMMAND_TYPE_MISSION_DOWNLINK, mission_start_time, mission_object.image_count,
        mission_object.interval, downlink_start_time)

    # Stop beacon from using serial port via pipe
    pipe.send("close_serial")
    while pipe.poll() == "":
        pass
    print(f"process receive {pipe.recv()}")

    # Start creating serial object
    ttnc_serial = setup_serial(ttnc_serial_port)

    # Send misison telecommand to Cubesat
    print(f"telecommand is {ccsds_mission_telecommand}")
    print(f"telecommand len is {len(ccsds_mission_telecommand)}")
    ttnc_serial.write(ccsds_mission_telecommand)

    # Return serial port to beacon process
    print("done sending command")
    ttnc_serial.close()
    pipe.send("open_serial")


# Process to handle downlink
def process_handle_downlink(payload_serial_port, pipe_beacon):

    # Setup serial object to reach ttnc transceiver
    def setup_serial(port):
        ser = serial.Serial(port)
        ser.baudrate = 115200
        ser.timeout = None  # Cannot set as nonblocking
        return ser

    # Create CCSDS Decoder
    ccsds_decoder = CCSDS_Decoder(isBeacon=False, isHK=False)

    # Setup payload serial port
    payload_serial = setup_serial(payload_serial_port)

    # ---------------------------------------------------------------
    # Receive all images
    recv_image_packets_list = []
    total_bytes_recv = 0
    image_collected_count = 0
    transfer_start = datetime.datetime.now()
    while True:
        # Wait for start packet
        print("Waiting for start packet")
        start_packet = payload_serial.read(mission_params.TOTAL_PACKET_LENGTH)

        # No more start packet
        if start_packet == b"":
            break
        # Start packet received
        else:
            payload_serial.timeout = 300  # Timeout after 300 sec if stuck
            image_collected_count += 1
            print(f"Start packet for image {image_collected_count} received")

        # Extract out useful data from padded packet
        start_packet_data = start_packet[:13]
        total_batch_expected = int.from_bytes(start_packet_data[10:], 'big')
        print(f"Total batches: {total_batch_expected} for image {image_collected_count}")

        recv_packets_list = []
        is_packet_failed = False
        is_last_packet = False
        prev_success_packet_num = 0

        # Receive all batches of image
        while True:
            ser_bytes = payload_serial.read(mission_params.TOTAL_PACKET_LENGTH)
            ret = ccsds_decoder.quick_parse_downlink(ser_bytes)
            total_bytes_recv += len(ser_bytes)

            # ---------------------------------------------------------------
            # Decoding packet
            # ---------------------------------------------------------------

            # Failed to receive current packet
            if ret['fail'] == True:
                print(ret)
                is_packet_failed = True

            # Successfully received current packet
            else:
                # If packet is a resend
                if ret['curr_batch'] == prev_success_packet_num:
                    is_packet_failed = False

                # If new packet
                else:
                    prev_success_packet_num = ret['curr_batch']

                    # Append received packet to list
                    recv_packets_list.append(ser_bytes)
                    print(f"Append - {ret}")

                    # Flag to indicate successfully received packet
                    is_packet_failed = False

            # ---------------------------------------------------------------
            # Handle Ack/Nack
            # ---------------------------------------------------------------

            # Send nack
            if is_packet_failed:
                return_val = b"nack\r\n"

            # Send ack
            else:
                return_val = b"ack\r\n"

            time.sleep(mission_params.TIME_BEFORE_ACK)
            payload_serial.write(return_val)
            print(f"Sent {return_val}")
            print()

            # Needs this line to stop the last packet < 149 bytes
            if ret['fail'] == False and ret['curr_batch'] == total_batch_expected - 2:
                payload_serial.timeout = mission_params.TIMEOUT_LAST_PACKET

            if ret['fail'] == False and ret['curr_batch']+1 == total_batch_expected:
                print(f"last packet - {ret['curr_batch']}\n")
                is_last_packet = True

            if is_last_packet == True:
                break

        # Append list of image packets found to main list
        recv_image_packets_list.append(recv_packets_list)

        # Change timeout between images
        payload_serial.timeout = mission_params.TIME_BETWEEN_IMAGES_GROUND

    transfer_end = datetime.datetime.now()
    elapsed_time_sec = (transfer_end - transfer_start).total_seconds()
    data_rate_kbps = (total_bytes_recv*8/elapsed_time_sec)/(2**10)
    print(f"Collected {total_bytes_recv/(2 ** 10):.2f} KB")
    print(f"Time elapsed: {elapsed_time_sec:.2f} sec")
    print(f"Downlink rate: {data_rate_kbps:.2f} Kbps")

    # ---------------------------------------------------------------

    curr_image_count = 1
    for recv_image_packets in recv_image_packets_list:
        # Reassemble packets to image
        # TODO: Save to specific mission folder later
        with open(f"{mission_params.GROUND_STN_MISSION_FOLDER_PATH}/out.gz", "wb") as enc_file:
            for packet in recv_image_packets:
                try:
                    enc_file.write(ccsds_decoder.parse_downlink_packet(packet))
                except ReedSolomonError:
                    print("Failed to decode as too many errors in packet")
                    continue  # Skip to next image
            enc_file.close()

        # TODO: Indicate success/fail action

        # For linux
        if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            os.chmod("decode.sh", 0o777)
            subprocess.Popen("./decode.sh out out", shell=True)

        # For windows
        elif sys.platform.startswith('win'):
            # Assumes cygwin installed in correct filepath
            is_cygwin_exist = os.path.isdir(r"C:\cygwin64\bin")
            is_gzip_exist = os.path.exists(r"C:\cygwin64\bin\gzip.exe")
            is_rm_exist = os.path.exists(r"C:\cygwin64\bin\rm.exe")

            if is_cygwin_exist and is_gzip_exist and is_rm_exist:
                # TODO: Handle error messages from processes
                subprocess.Popen(r"C:\cygwin64\bin\gzip.exe -d mission/out.gz", shell=True)
                time.sleep(1)

                with open(f'{mission_params.GROUND_STN_MISSION_FOLDER_PATH}/out', 'rb') as enc_file:
                    bin_file = enc_file.read()
                enc_file.close()

                with open(f'{mission_params.GROUND_STN_MISSION_FOLDER_PATH}/out.jpg', 'wb') as output:
                    # TODO: Handle error messages from processes
                    output.write(base64.b64decode(bin_file))

                # Remove out file
                subprocess.Popen(r"C:\cygwin64\bin\rm.exe mission/out", shell=True)

            # cygwin not exist
            else:
                pass

        # For mac
        elif sys.platform.startswith('darwin'):
            pass

        # Rename image file
        if os.path.exists("mission/out.jpg"):
            try:
                os.rename("mission/out.jpg", f"mission/out_{curr_image_count}.jpg")
            except FileExistsError:
                print("duplicate file found!")
                continue

        # Increment image count
        curr_image_count += 1

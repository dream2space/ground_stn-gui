import base64
import datetime
import os
import random
import subprocess
import sys
import time

import serial
from reedsolo import ReedSolomonError

import CCSDS_Parameters as ccsds_params
import Mission_Parameters as mission_params
from CCSDS_Decoder import CCSDS_Decoder
from CCSDS_Encoder import CCSDS_Encoder
from CCSDS_HK_Util import CCSDS_HK_Util
from Testing import IS_TESTING


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # pylint: disable=no-member
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def beacon_collection(pipe_beacon):
    """
    Collects beacons inputs from serial ports and sends out via pipes to GUI.

    Args:
        pipe_beacon (Connection): Pipe to send out beacon inputs collected.
    """

    def setup_serial(port):
        ttnc_ser = serial.Serial(port)
        ttnc_ser.baudrate = 9600
        ttnc_ser.timeout = 0.8
        return ttnc_ser

    # Setup CCSDS Decoder
    Decoder = CCSDS_Decoder(isBeacon=True, isHK=False)

    while pipe_beacon.poll() == b"":
        pass

    # Obtain ttnc serial port object
    ttnc_serial_port = pipe_beacon.recv()

    # Setup ttnc port serial object
    if not IS_TESTING:
        ttnc_ser = setup_serial(ttnc_serial_port)
        print("first setup serial done")

    # Setup ttnc serial port
    temp = 0
    gx = 0
    gy = 0
    gz = 0
    pipe_beacon.send([temp, gx, gy, gz])

    isStopBeacon = False
    while True:

        if IS_TESTING:
            temp = f"{random.randrange(20, 40)}"
            gx = f"{random.randint(-50, 50)}"
            gy = f"{random.randint(-50, 50)}"
            gz = f"{random.randint(-50, 50)}"
            print("beacon", temp, gx, gy, gz)
            time.sleep(10)
            pipe_beacon.send([temp, gx, gy, gz])
            continue

        # If receive signal to close serial port
        if pipe_beacon.poll() == True:
            recv = pipe_beacon.recv()
            print(f"beacon process {recv}")

            if recv == "close_serial":
                ttnc_ser.close()
                pipe_beacon.send("done")
                isStopBeacon = True
                print("close serial")

            if recv == "open_serial":
                ttnc_ser = setup_serial(ttnc_serial_port)
                isStopBeacon = False

        if not isStopBeacon:
            # Read beacon packets
            # print("reading beaconds")
            ccsds_beacon_bytes = ttnc_ser.read(
                ccsds_params.CCSDS_BEACON_LEN_BYTES)
            # print(ccsds_beacon_bytes)
            # lock.release()

            if ccsds_beacon_bytes:
                try:
                    decoded_ccsds_beacon = Decoder.parse_beacon(
                        ccsds_beacon_bytes)
                except IndexError:
                    continue

                temp = f"{decoded_ccsds_beacon.get_temp():.2f}"
                gyro = decoded_ccsds_beacon.get_gyro()
                gx = f"{gyro['gx']}"
                gy = f"{gyro['gy']}"
                gz = f"{gyro['gz']}"

                # print("beacon", temp, gx, gy, gz)
                pipe_beacon.send([temp, gx, gy, gz])


# Process to get housekeeping logs
def process_get_HK_logs(pipe, ttnc_serial_port):

    def setup_serial(port):
        ttnc_ser = serial.Serial(port)
        ttnc_ser.baudrate = 9600
        ttnc_ser.timeout = 10
        return ttnc_ser

    Encoder = CCSDS_Encoder()
    HK_Util = CCSDS_HK_Util()

    # Default for command
    timestamp_query_start = '0-0-0-0-0-0'
    timestamp_query_end = '0-0-0-0-0-0'

    telecommand = Encoder.generate_HK_telecommand(
        ccsds_params.TELECOMMAND_TYPE_OBC_HK_REQUEST, timestamp_query_start, timestamp_query_end)

    pipe.send("close_serial")
    while pipe.poll() == "":
        pass
    print(f"process receive {pipe.recv()}")

    ttnc_serial = setup_serial(ttnc_serial_port)

    print(f"telecommand is {telecommand}")
    print(f"telecommand len is {len(telecommand)}")
    ttnc_serial.write(telecommand)
    hk_bytes = ttnc_serial.read(
        ccsds_params.CCSDS_OBC_TELEMETRY_LEN_BYTES)
    # print(f"hk bytes {hk_bytes}")

    print("done sending command")
    ttnc_serial.close()
    pipe.send("open_serial")

    if hk_bytes:
        list_hk_obj = HK_Util.parse(hk_bytes)
        HK_Util.log(list_hk_obj)
        print("done do logs")
    else:
        print("hk logs failed")


# Sample process to run in place of HK telecommand in testing mode
def sample_hk_command_process():
    i = 0
    max_val = 50000

    while i < max_val:
        print(i)
        i += 1


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
        ttnc_ser = serial.Serial(port)
        ttnc_ser.baudrate = 115200
        ttnc_ser.timeout = None  # Cannot set as nonblocking
        return ttnc_ser

    # Disable beacons
    pipe_beacon.send("close_serial")
    while pipe_beacon.poll() == "":
        pass
    print(f"process receive {pipe_beacon.recv()}")

    # Create CCSDS Decoder
    ccsds_decoder = CCSDS_Decoder(isBeacon=False, isHK=False)

    # Setup payload serial port
    payload_serial = setup_serial(payload_serial_port)

    # Wait for start packet
    print("Waiting for start")
    start_packet = payload_serial.read(mission_params.TOTAL_PACKET_LENGTH)

    # Extract out useful data from padded packet
    start_packet_data = start_packet[:13]
    total_batch_expected = int.from_bytes(start_packet_data[10:], 'big')
    print(f"Total batches: {total_batch_expected}")

    recv_packets = []
    is_packet_failed = False
    is_last_packet = False
    prev_success_packet_num = 0

    # Receive all batches
    transfer_start = datetime.datetime.now()
    while True:
        ser_bytes = payload_serial.read(mission_params.TOTAL_PACKET_LENGTH)

        # Exit loop after final batch
        if ser_bytes == b"" and len(recv_packets) == total_batch_expected:
            break

        elif ser_bytes == b"" and len(recv_packets) < total_batch_expected:
            # resend n/ack
            return_val = b"nack\r\n"

        ret = ccsds_decoder.quick_parse_downlink(ser_bytes)

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
                recv_packets.append(ser_bytes)
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
            payload_serial.timeout = mission_params.TIMEOUT_TX * 0.75

        if ret['fail'] == False and ret['curr_batch']+1 == total_batch_expected:
            print(f"last packet - {ret['curr_batch']}")
            is_last_packet = True

        if is_last_packet == True:
            break

    print(f"Collected {len(recv_packets)} packets")
    transfer_end = datetime.datetime.now()
    elapsed_time = transfer_end - transfer_start
    print(f"Time elapsed: {elapsed_time}")

    # Reassemble packets to image
    with open(f"{mission_params.GROUND_STN_MISSION_FOLDER_PATH}/out.gz", "wb") as enc_file:
        for packet in recv_packets:
            try:
                enc_file.write(ccsds_decoder.parse_downlink_packet(packet))
            except ReedSolomonError:
                print("Failed to decode as too many errors in packet")
                return
        enc_file.close()

    # TODO: Check OS and prescribe decode steps

    # Works only in linux
    # os.chmod("decode.sh", 0o777)
    # subprocess.Popen("./decode.sh out out", shell=True)
    # print("Done!")

    # For windows:
    # Assumes cygwin installed in correct filepath
    # TODO: Change the mission directory/filename
    subprocess.Popen(r"C:\cygwin64\bin\gzip.exe -d mission/out.gz", shell=True)
    time.sleep(1)

    # TODO: Change the mission directory/filename
    with open('mission/out', 'rb') as enc_file:
        bin_file = enc_file.read()
    enc_file.close()
    # TODO: Change the mission directory/filename
    with open('mission/out.jpg', 'wb') as output:
        output.write(base64.b64decode(bin_file))

    # Remove out file
    # TODO: Change the mission directory/filename
    subprocess.Popen(r"C:\cygwin64\bin\rm.exe mission/out", shell=True)

    # TODO: Indicate success/fail action

    print("done sending command")
    pipe_beacon.send("open_serial")

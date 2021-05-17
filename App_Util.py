# Serial port scan
import serial
import glob
import sys


# Testing flag
from Testing import IS_TESTING
from CCSDS_Decoder import CCSDS_Decoder
import CCSDS_Parameters as ccsds_params
import random
import time


def scan_serial_ports():
    """
    Scans for serial ports currently open and returns as a list.

    Returns:
        list: List of serial ports as Strings
    """
    ports = []
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    # else:
    #     raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


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
    Decoder = CCSDS_Decoder(isBeacon=True)

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

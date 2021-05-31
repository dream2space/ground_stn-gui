GROUND_STN_MISSION_FOLDER_PATH = 'mission'

#### DOWNLINK CONSTANTS ####
# BATCH_SIZE = 5
BATCH_SIZE = 1
PRE_ENC_CHUNK_SIZE = 120  # bytes, w/o 16 bytes rs encoding yet
TELEMETRY_PACKET_TYPE_DOWNLINK_START = 30
TELEMETRY_PACKET_TYPE_DOWNLINK_PACKET = 31
TELEMETRY_PACKET_TYPE_DOWNLINK_STOP = 32

TOTAL_PACKET_LENGTH = 149
HEADER_LENGTH = 6
TELEMETRY_TYPE_LENGTH = 1  # bytes
TOTAL_BYTES_LENGTH = 3
TOTAL_BATCH_LENGTH = 3

TELEMETRY_TYPE_LENGTH = 1  # bytes
CURRENT_CHUNKS_LENGTH = 3
CURRENT_BATCH_LENGTH = 3
TOTAL_BYTES_LENGTH = 3
TOTAL_BATCH_LENGTH = 3

TIME_SLEEP_AFTER_START = 2
TIME_BEFORE_ACK = 0.04
TIME_BETWEEN_PACKETS = TIME_BEFORE_ACK
TIME_BETWEEN_IMAGES_PAYLOAD = 2
# TIME_BETWEEN_IMAGES_GROUND = TIME_BETWEEN_IMAGES_PAYLOAD * 2

TIMEOUT_TX = 0.9  # Cut down ack timeout for faster response
TIMEOUT_RX = TIME_SLEEP_AFTER_START

TIMEOUT_LAST_PACKET = TIMEOUT_TX * 0.75

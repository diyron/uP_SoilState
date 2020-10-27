######################################################################
# LORA

import ujson
from libs.ulora import uLoRa, TTN

# Refer to device pinout / schematics diagrams for pin details

LORA_CS = const(18)
LORA_SCK = const(5)
LORA_MOSI = const(27)
LORA_MISO = const(19)
LORA_IRQ = const(26)
LORA_RST = const(14)

LORA_DATARATE = "SF9BW125"  # Choose from several available
FPORT = 1

# From TTN console for device
# msb
DEVADDR = bytearray([0x01, 0xd1, 0x51, 0x52])

# msb
NWSKEY = bytearray([0x4d, 0x70, 0xe1, 0x85, 0x8e, 0xc6, 0xda, 0x11, 0x5d, 0x81, 0x6f, 0x22, 0x7e, 0xbf, 0x15, 0x8e])

# msb
APPSKEY = bytearray([0x54, 0xad, 0xd4, 0x4f, 0x8c, 0xbe, 0xbf, 0x8a, 0xab, 0x55, 0x5f, 0x41, 0xc0, 0x34, 0xc5, 0xf0])

TTN_CONFIG = TTN(DEVADDR, NWSKEY, APPSKEY, country="EU")

lora = uLoRa(
    cs=LORA_CS,
    sck=LORA_SCK,
    mosi=LORA_MOSI,
    miso=LORA_MISO,
    irq=LORA_IRQ,
    rst=LORA_RST,
    ttn_config=TTN_CONFIG,
    datarate=LORA_DATARATE,
    fport=FPORT
)

# testdata = {"key1": "Hello",
#             "key2": "World!"}
#
# data = ujson.dumps(testdata)  # dictionary to json
# buf = bytearray(data, 'utf-8')

data_list = [0x10,0x20]
buf = bytearray(data_list)
print(buf)
print("send data")
# ...Then send data as bytearray

lora.send_data(buf, len(buf), lora.frame_counter)
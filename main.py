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

######################################################################

data_dict = {
    "vbat": 0,
    "chrg": False,
    "tsys": 0,
    "soil": 0,
    "t_05": 0,
    "t_20": 0
}

from machine import ADC, Pin
def get_vbat():
    adc = ADC(Pin(38))  # create ADC object on ADC pin
    adc.atten(ADC.ATTN_6DB)  # set 6dB input attenuation (voltage range roughly 0.0v - 2.0 v)
    adc.width(ADC.WIDTH_12BIT)  # set 12 bit return values (returned range 0-4095)
    v_raw = adc.read()
    return v_raw  # calculate vbat


def get_chargestate():
    pin_ok = Pin(17, Pin.IN)   # GPIO 17 - in - OK(green)
    pin_ch = Pin(16, Pin.IN)   # GPIO 16 - in - CHRG(red)
    return pin_ch.value()


import esp32
def get_temp_system():
    t_raw = esp32.raw_temperature()  # read the internal temperature of the MCU, in Farenheit
    return t_raw  # calculate temp in C


import time
def get_soil_value():
    pin_en = Pin(0, Pin.OUT)  # GPIO 37 - out - VCC
    pin_en.on()  # set pin to "on" (high) level

    adc = ADC(Pin(36))  # GPIO 36 - in - ADC
    adc.atten(ADC.ATTN_6DB)  # set 6dB input attenuation (voltage range roughly 0.0v - 2.0 v)
    adc.width(ADC.WIDTH_12BIT)  # set 12 bit return values (returned range 0-4095)
    soil_raw = adc.read()
    time.sleep_ms(200)  # wait for adc and sensor
    soil_raw = adc.read()
    soil_raw = adc.read()

    pin_en.off()  # set pin to "off" (low) level

    return soil_raw  # calculate soil value


import time
import ds18x20
import onewire
ow = onewire.OneWire(Pin(12))  # create a OneWire bus on GPIO12
ds = ds18x20.DS18X20(ow)
rom_t5 = ""
rom_t20 = ""

def get_soil_temp(ow_ds,rom):
    ow_ds.convert_temp()
    time.sleep_ms(750)
    t_raw = ow_ds.read_temp(rom)
    return t_raw # calulate temp

######################################################################
from libs.ulora import uLoRa, TTN  # LORA
from machine import ADC, Pin
import machine
import esp32
import time
import ds18x20
import onewire
######################################################################
# From TTN console for device (all # msb)
DEVADDR = bytearray([0x01, 0xd1, 0x51, 0x52])
NWSKEY = bytearray([0x4d, 0x70, 0xe1, 0x85, 0x8e, 0xc6, 0xda, 0x11, 0x5d, 0x81, 0x6f, 0x22, 0x7e, 0xbf, 0x15, 0x8e])
APPSKEY = bytearray([0x54, 0xad, 0xd4, 0x4f, 0x8c, 0xbe, 0xbf, 0x8a, 0xab, 0x55, 0x5f, 0x41, 0xc0, 0x34, 0xc5, 0xf0])
TTN_CONFIG = TTN(DEVADDR, NWSKEY, APPSKEY, country="EU")

LORA_DATARATE = "SF9BW125"  # Choose from several available
# Refer to device pinout / schematics diagrams for pin details
lora = uLoRa(cs=18, sck=5, mosi=27, miso=19, irq=26, rst=14, ttn_config=TTN_CONFIG, datarate=LORA_DATARATE, fport=1)
######################################################################

def get_values():
    data_dict = {}

    # vbat
    adc = ADC(Pin(38))  # create ADC object on ADC pin
    adc.atten(ADC.ATTN_6DB)  # set 6dB input attenuation (voltage range roughly 0.0v - 2.0 v)
    adc.width(ADC.WIDTH_12BIT)  # set 12 bit return values (returned range 0-4095)
    v_raw = adc.read()
    data_dict["vbat"] = v_raw # calculate vbat

    #chargestate
    pin_ok = Pin(17, Pin.IN)   # GPIO 17 - in - OK(green)
    pin_ch = Pin(16, Pin.IN)   # GPIO 16 - in - CHRG(red)
    if pin_ch.value():
        data_dict["chrg"] = 1
    else:
        data_dict["chrg"] = 0

    # system temperature
    t_raw = esp32.raw_temperature()  # read the internal temperature of the MCU, in Farenheit
    data_dict["tsys"] = t_raw

    # soil humi
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
    data_dict["soil"] = soil_raw  # calculate soil value

    # onwire
    ow = onewire.OneWire(Pin(12))  # create a OneWire bus on GPIO12
    ds = ds18x20.DS18X20(ow)
    rom_t5 = ""
    rom_t20 = ""

    # onewire 5 cm
    ds.convert_temp()
    time.sleep_ms(750)
    t5_raw = ds.read_temp(rom_t5)
    data_dict["t5"] = t5_raw

    # onewire 5 cm
    ds.convert_temp()
    time.sleep_ms(750)
    t20_raw = ds.read_temp(rom_t20)
    data_dict["t20"] = t20_raw

    print(data_dict)
    for k, v in data_dict:
        print(k, v)

    return data_dict

######################################################################
# check if the device woke from a deep sleep

def send_data(lora_instance,data):

    data_list = []
    for k, v in data:
        print(k, v)
        data_list.append(v)

    buf = bytearray(data_list)
    print(buf)
    print("send data")
    # ...Then send data as bytearray
    lora.send_data(buf, len(buf), lora.frame_counter)


# sleep_cnt = 0
# deepsleep_ms = const(60000)
# deepsleep_minutes = const(10)
#
#
# if machine.reset_cause() == machine.DEEPSLEEP_RESET:
#     print('woke from a deep sleep')
#     if sleep_cnt == deepsleep_minutes:
#         sleep_cnt = 0
#         # send_data(lora_instance=lora, data=get_values())
#         machine.deepsleep(deepsleep_ms)
#     else:
#         sleep_cnt += 1
#         print("")
# else:
#     # put the device to sleep for 60 seconds
#     machine.deepsleep(deepsleep_ms)




from time import sleep
from machine import Pin, SPI
import struct

PRINT_RAW = False

sck_pin = Pin(19, value=0)  # Brown wire, connector pin 1
ss_pin = Pin(21, Pin.OUT, value=1)  # Red wire, connector pin 2
miso_pin = Pin(18)  # Orange wire, connector pin 3
mosi_pin = Pin(5)  # Unconected

spi = SPI(
    1,
    baudrate=1_000_000,
    polarity=0,
    phase=1,
    sck=sck_pin,
    mosi=mosi_pin,
    miso=miso_pin,
)


def read_sensor():
    # Read 2 bytes from the sensor
    ss_pin.value(0)
    data = spi.read(2)
    ss_pin.value(1)

    # Convert the 2 bytes to a 16-bit number
    decoded = struct.unpack("!H", data)[0]

    # Discard the first two bits, which are used for parity errors
    decoded = decoded >> 2

    # Extract the alarm bits for magnetic field too high or too low
    alarm = (decoded & (0b11 << 12)) >> 12
    if alarm & 1:
        high = "H"
    else:
        high = " "
    if alarm & 2:
        low = "L"
    else:
        low = " "

    # Keep the 12 bits of data
    decoded = decoded & 0xFFF

    # Sometimes, the decoded signal is zero, why ?
    if decoded == 0:
        return

    if PRINT_RAW:
        print("{}{} {:05d}".format(high, low, decoded))
    else:
        angle = int(360.0 * decoded / 4096.0)
        print("{:03d}".format(angle))


while True:
    read_sensor()
    sleep(0.01)

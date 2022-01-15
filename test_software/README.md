# ESP32 firmware to test the board

`ams.py` contains [MicroPython](https://docs.micropython.org/en/latest/esp32/quickref.html) code to test the angle sensor.
It will read the sensor's output and print in in the terminal.
To run it, after installing MicroPython on the ESP32, run the following command on your computer:

```shell
./pyboard.py ams.py --device /dev/tty.SLAB_USBtoUART
```

You can interrupt it by pressing Ctrl-C.

# inky-cryptochart

CLI tool to display cryptocurrency candlestick chart on [Pimoroni Inky pHAT](https://shop.pimoroni.com/products/inky-phat) or [Waveshare 2.13inch E-Ink display HAT](https://www.waveshare.com/2.13inch-e-paper-hat-b.htm)

![](https://github.com/DurandA/inky-cryptochart/wiki/images/inky-cryptochart.jpg)

04b03 freeware font by [04](http://www.04.jp.org/).

## Setup

This is the setup for a Raspberry Pi OS (Bullseye) but it should be similar with other systems.

Enable SPI using `raspi-config` (`Interfacing Options` > `SPI`).

Install required dependencies:

```sh
sudo apt install git python3-pip python3-dev libatlas-base-dev libopenjp2-7
```

### Inky pHAT display

```sh
pip install git+https://github.com/DurandA/inky-cryptochart.git#egg=cryptochart[inky]
cryptochart --driver inky
```

### Wavehsare display

```sh
git clone https://github.com/waveshare/e-Paper
cd e-Paper/RaspberryPi_JetsonNano/python && pip install .
pip install git+https://github.com/DurandA/inky-cryptochart.git#egg=cryptochart[waveshare_epd]
cryptochart --driver waveshare_epd
```

If you have issues, check that you use the correct driver for your display (`epd2in13_V2` by default).

Alternatively, you can use the `inky` driver and redifine the pins on the `inky212x104` module:

```diff
-RESET_PIN = 27
+RESET_PIN = 17
-BUSY_PIN = 17
+BUSY_PIN = 24
-DC_PIN = 22
+DC_PIN = 25
```

### Add your own driver

If you use a different display, you can easily add your own driver in `cryptochart/cli.py` by implementing `set_image()` and `show()`:

```python
class MyDriver():
    def __init__(self, *args):
        pass

    def set_image(self, image):
        # store the image on buffer

    def show(self):
        # draw the image on display from buffer
```

You also need to adjust width and height (in pixels) in `cryptochart/__init__.py` to fit the display.

## Usage

```
usage: cryptochart [-h] [--driver {inky,inkyphat,waveshare_epd}] [--pair PAIR]
                   [--flip] [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  --driver {inky,inkyphat,waveshare_epd}
  --pair PAIR           currency pair (default: XETHZUSD)
  --flip                rotate the display (default: False)
  --output OUTPUT       save plot as png (default: None)
```

## Configure crontab

Use `crontab -e` to add run the cronjob every 15 minutes:

```
*/15 * * * * cryptochart --driver inky --pair XETHZUSD
```

If you are not familiar with cron, have a look at the excellent [CronHowto](https://help.ubuntu.com/community/CronHowto) wiki to configure it according to your requirements.

## Put you Rasberry Pi in read-only mode

Chances are that you SD card will get quickly corrupted if you unplug your Raspberry Pi without proper shutdown. To prevent this, you can [configure the OS for read-only mode](https://learn.adafruit.com/read-only-raspberry-pi).

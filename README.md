# inky-cryptochart

CLI tool to display cryptocurrency candlestick chart on [Pimoroni Inky pHAT](https://shop.pimoroni.com/products/inky-phat) or [Waveshare 2.13inch E-Ink display HAT](https://www.waveshare.com/2.13inch-e-paper-hat-b.htm)

![](http://redcorner.io/images/inky-cryptochart.jpg)

04b03 freeware font by [04](http://www.04.jp.org/).

## Setup

Install the `inky-phat` prerequisites (see [official instructions](https://github.com/pimoroni/inky-phat#installing)):

```
sudo apt-get install python3-pip python3-dev
```

Install required packages:

```
sudo pip3 install -r requirements.txt
```

### Wavehsare

The Waveshare HAT requires an extra step since it has a slightly different pinout. You can redifine the pins on the `inky212x104` module:

```diff
-RESET_PIN = 27
+RESET_PIN = 17
-BUSY_PIN = 17
+BUSY_PIN = 24
-DC_PIN = 22
+DC_PIN = 25
```

## Usage

```
usage: cryptochart.py [-h] [--pair PAIR] [--flip] [--output OUTPUT]

optional arguments:
  -h, --help       show this help message and exit
  --pair PAIR      currency pair (default: XETHZUSD)
  --flip           rotate the display (default: False)
  --output OUTPUT  save plot as png (default: None)
```

## Configure crontab

Use `crontab -e` to add run the cronjob every 15 minutes:

```
*/15 * * * * (cd /home/user/inky-cryptochart; python3 cryptochart.py --pair XETHZUSD --flip)
```

If you are not familiar with cron, have a look at the excellent [CronHowto](https://help.ubuntu.com/community/CronHowto) wiki to configure it according to your requirements.

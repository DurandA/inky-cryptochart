# inky-cryptochart

CLI tool to display cryptocurrency candlestick chart on Inky pHAT

![](http://redcorner.io/images/inky-cryptochart.jpg)

04b03 freeware font by [04](http://www.04.jp.org/).

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

Allow file execution with `chmod +x cryptochart.py` and use `crontab -e` to add run the cronjob every 15 minutes:

```
*/15 * * * * /home/user/cryptochart/cryptochart.py --pair XETHZUSD
```

If you are not familiar with cron, have a look at the excellent [CronHowto](https://help.ubuntu.com/community/CronHowto) wiki to configure it according to your requirements.

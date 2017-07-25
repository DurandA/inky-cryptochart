#!/usr/bin/env python3

import argparse, io
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import font_manager
try:
    from mpl_finance import candlestick_ohlc
except ImportError:
    from matplotlib.finance import candlestick_ohlc
from PIL import Image, ImageFont
import requests

from cryptochart.providers import quotes_historical_kraken_ohlc

parser = argparse.ArgumentParser()
parser.add_argument("--output", help="save plot as png")
args = parser.parse_args()

yesterday = datetime.now() - timedelta(hours=12)
unix_time = yesterday.strftime("%s")
payload = {'pair': 'XETHZUSD', 'since': unix_time, 'interval': 15}
r = requests.get('https://api.kraken.com/0/public/OHLC', params=payload)

def sanitize_ohlc(data):
    return [[int(l[0]), float(l[1]), float(l[2]), float(l[3]), float(l[4])] for l in data]

quotes = sanitize_ohlc(r.json()['result']['XETHZUSD'])
if len(quotes) == 0:
    raise SystemExit

w, h = (212, 104)
dpi = 144
fig, ax = plt.subplots(figsize=(212/dpi, 104/dpi), dpi=dpi)
fig.subplots_adjust(top=1, bottom=0, left=0.15, right=1)

ticks_font = font_manager.FontProperties(fname='04B_03__.TTF', size=4)
plt.rcParams['text.antialiased'] = False

for label in ax.get_yticklabels() :
    label.set_fontproperties(ticks_font)
ax.yaxis.set_tick_params(pad=2)

#ax.tick_params(labelsize=8)
ax.xaxis.set_ticks([])
#ax.xaxis.set_visible(False)
ax.set_frame_on(False)
#ax.set_axis_off()
#ax.axis('off')

candlestick_ohlc(ax, quotes, width=1)

ax.xaxis_date()
ax.autoscale_view()

ymin, ymax = ax.get_ylim()
last_low = quotes[-1][3]
last_high = quotes[-1][2]

ypos = 12 if ymax - last_high > last_low - ymin else h

font = ImageFont.truetype('04B_03__.TTF', 4)

print(ypos)
if args.output:
    fig.savefig(args.output, dpi=dpi, cmap="bwr", interpolation="none", origin="lower", pad_inches=0)#bbox_inches='tight')
else:
    import inkyphat
    with io.BytesIO() as f:
        fig.savefig(f, dpi=dpi, cmap="bwr", interpolation="none", origin="lower", pad_inches=0)
        f.seek(0)
        i = Image.open(f)
        inkyphat.set_image(i)
        inkyphat.text((170, ypos), quotes[-1][4], inkyphat.RED, font)
        inkyphat.text((180, ypos), 'XETHZUSD', inkyphat.BLACK, font)
        inkyphat.show()
#plt.show()

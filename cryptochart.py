#!/usr/bin/env python3
from cryptochart import ax, fig, w, h, dpi
from cryptochart.providers import quotes_historical_kraken_ohlc
import argparse, io
from datetime import datetime, timedelta

try:
    from mpl_finance import candlestick_ohlc
except ImportError:
    from matplotlib.finance import candlestick_ohlc
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--pair", default="XETHZUSD", help="currency pair")
parser.add_argument(
    "--flip", dest="flip", action="store_true", help="rotate the display"
)
parser.set_defaults(flip=False)
parser.add_argument("--output", help="save plot as png")
parser.add_argument(
    "--colour",
    default="black",
    choices=["red", "black", "yellow"],
    help="ePaper display colour",
)
args = parser.parse_args()

yesterday = datetime.now() - timedelta(hours=12)

quotes = quotes_historical_kraken_ohlc(args.pair, yesterday, interval=15)
if len(quotes) == 0:
    raise SystemExit

candlestick_ohlc(ax, quotes, width=1)

ax.xaxis_date()
ax.autoscale_view()

ymin, ymax = ax.get_ylim()

last_low = quotes[-1][3]
last_high = quotes[-1][2]
last_close = quotes[-1][4]

font = ImageFont.truetype("04B_03__.TTF", 8)

BLACK = (0, 0, 0)

if args.colour == "red":
    PAIR_COLOR = (255, 0, 0)
elif args.colour == "yellow":
    PAIR_COLOR = (255, 255, 0)
else:
    PAIR_COLOR = (0, 0, 0)

with io.BytesIO() as f:
    fig.savefig(
        f, dpi=dpi, cmap="bwr", interpolation="none", origin="lower", pad_inches=0
    )  # bbox_inches='tight')
    f.seek(0)
    img = Image.open(f)  # .convert('P', palette=(0,1,2))
    draw = ImageDraw.Draw(img)
    ypos = 0 if ymax - last_high > last_low - ymin else h - 6

    if not args.output:
        from inky import InkyPHAT

        inky_display = InkyPHAT(args.colour)
        inky_display.set_border(inky_display.BLACK)

        # ensure the image is using the correct pallet
        pal_img = Image.new("P", (1, 1))
        pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)
        img = img.convert("RGB").quantize(palette=pal_img)

        inky_display.set_image(img)
        if args.flip:
            inky_display.set_rotation(180)
    else:
        text = draw.text

    draw.text((148, ypos), "{:.2f}".format(last_close), BLACK, font)
    draw.text((176, ypos), args.pair, PAIR_COLOR, font)

    if args.output:
        img.save(args.output)
        raise SystemExit

    inky_display.show()

#!/usr/bin/env python3
from cryptochart import ax, fig, w, h, dpi
from cryptochart.providers import quotes_historical_kraken_ohlc
import argparse, io
from datetime import datetime, timedelta
try:
    from mplfinance.original_flavor import candlestick_ohlc
except ImportError:
    from matplotlib.finance import candlestick_ohlc
from PIL import Image, ImageDraw, ImageFont

def main(use_inky=True):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--pair", default='XETHZUSD', help="currency pair")
    parser.add_argument('--flip', dest='flip', action='store_true', help="rotate the display")
    parser.set_defaults(flip=False)
    parser.add_argument("--output", help="save plot as png")
    args = parser.parse_args()

    yesterday = datetime.now() - timedelta(hours=12)

    quotes = quotes_historical_kraken_ohlc(args.pair, yesterday, interval=15)
    if not quotes:
        raise ValueError('Empty OHLC data')

    candlestick_ohlc(ax, quotes, width=1)

    ax.xaxis_date()
    ax.autoscale_view()

    ymin, ymax = ax.get_ylim()

    last_low = quotes[-1][3]
    last_high = quotes[-1][2]
    last_close = quotes[-1][4]

    font = ImageFont.truetype('04B_03__.TTF', 8)

    with io.BytesIO() as f:
        fig.savefig(f, dpi=dpi, cmap="bwr", interpolation="none", origin="lower", pad_inches=0)
        f.seek(0)
        i = Image.open(f)
        d = ImageDraw.Draw(i)
        ypos = 0 if ymax - last_high > last_low - ymin else h - 6

        if not args.output:
            if not use_inky:
                from inkyphat import RED, BLACK, set_image as _set_image, show as _show
                class InkyPHAT():
                    def __init__(*args):
                        pass
                    set_image = staticmethod(_set_image)
                    show = staticmethod(_show)
            else:
                from inky import InkyPHAT

            display = InkyPHAT()
            display.set_image(i)

            if args.flip:
                i = i.transpose(Image.ROTATE_180)
        else:
            RED = (255,0,0)
            BLACK = (0,0,0)

        d.text((148, ypos), '{:.2f}'.format(last_close), BLACK, font)
        d.text((176, ypos), args.pair, RED, font)

        if args.output:
            i.save(args.output)
            return

        display.show()

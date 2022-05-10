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

from . import fonts, pkg_resources


def main(driver='inky'):
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

    ttf = pkg_resources.open_binary(fonts, '04B_03__.TTF')
    font = ImageFont.truetype(ttf, 8)

    RED = (255,0,0)
    BLACK = (0,0,0)

    with io.BytesIO() as f:
        fig.savefig(f, dpi=dpi, cmap="bwr", interpolation="none", origin="lower", pad_inches=0)
        f.seek(0)
        i = Image.open(f)
        d = ImageDraw.Draw(i)
        ypos = 0 if ymax - last_high > last_low - ymin else h - 6

        if driver:
            if driver == 'inky':
                from inky import InkyPHAT
                RED = InkyPHAT.RED
                BLACK = InkyPHAT.BLACK

                display = InkyPHAT('black')
            if driver == 'inkyphat':
                from inkyphat import RED as inky_RED, BLACK as inky_BLACK, set_image as _set_image, show as _show
                RED = inky_RED
                BLACK = inky_BLACK

                class InkyPHAT():
                    def __init__(*args):
                        pass
                    set_image = staticmethod(_set_image)
                    show = staticmethod(_show)

                display = InkyPHAT()
            if driver == 'waveshare_epd':
                from waveshare_epd import epd2in13_V2

                class EPD():
                    def __init__(self, *args):
                        self.epd = epd2in13_V2.EPD()
                        self.epd.init(self.epd.FULL_UPDATE)
                        self.buf = []
                    def set_image(self, image):
                        self.buf = self.epd.getbuffer(image)
                    def show(self):
                        self.epd.display(self.buf)

                display = EPD()

            display.set_image(i.convert("P"))

            if args.flip:
                i = i.transpose(Image.ROTATE_180)

        d.text((148, ypos), '{:.2f}'.format(last_close), BLACK, font)
        d.text((176, ypos), args.pair, RED, font)

        if args.output:
            i.save(args.output)
            return

        display.show()

if __name__ == "__main__":
    main()

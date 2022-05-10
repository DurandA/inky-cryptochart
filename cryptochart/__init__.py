from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import font_manager

try:
    import importlib.resources as pkg_resources
except ImportError:
    # try backported to PY<37 `importlib_resources`
    import importlib_resources as pkg_resources

from . import fonts


w, h = (212, 104)
dpi = 144
fig, ax = plt.subplots(figsize=(212/dpi, 104/dpi), dpi=dpi)
fig.subplots_adjust(top=1, bottom=0, left=0.15, right=1)

with pkg_resources.path(fonts, '04B_03__.TTF') as fpath:
    ticks_font = font_manager.FontProperties(fname=fpath, size=4)
plt.rcParams['text.antialiased'] = False

for label in ax.get_yticklabels() :
    label.set_fontproperties(ticks_font)
ax.yaxis.set_tick_params(pad=2, width=1)

#ax.tick_params(labelsize=8)
ax.xaxis.set_ticks([])
#ax.xaxis.set_visible(False)
ax.set_frame_on(False)
#ax.set_axis_off()
#ax.axis('off')

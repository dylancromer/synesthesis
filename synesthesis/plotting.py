import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rcParams['figure.dpi'] = 150
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'figure.autolayout': True})
import seaborn as sns
sns.set(
    style='whitegrid',
    font_scale=0.9,
    rc={'lines.linewidth': 1.4, 'lines.markersize': 1.6},
)
from jupyterthemes import jtplot
jtplot.style(theme='oceans16')
jtplot.style(context='notebook', fscale=1, spines=False, gridlines='--')
BGD = '#1b1e28'
style_dict = {
    'figure.edgecolor': BGD,
    'figure.facecolor': BGD,
    'axes.facecolor': BGD,
    'axes.edgecolor': BGD,
    'grid.color': BGD,
    'patch.edgecolor': BGD,
    'patch.facecolor': BGD,
    'savefig.facecolor': BGD,
    'savefig.edgecolor': BGD,
}
matplotlib.rcParams.update(style_dict)
from mpl_toolkits import mplot3d


color_vals = (33//1.2, 36//1.2, 48//1.2)
PLOT_BACKGROUND_COLOR = (color_vals[0]/255, color_vals[1]/255, color_vals[2]/255, 1)
COLOR = '#46a5ce'
ALPHA = 0.4
ELEV = None
AZIM = 45
NUM_WIRES = 100


def plot_spectrum(times, freqs, spectrum, azimuth, outfile):
    X, Y = np.meshgrid(freqs, times)
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(X, Y, spectrum, color=COLOR, alpha=ALPHA, rcount=NUM_WIRES, ccount=NUM_WIRES)
    ax.w_xaxis.set_pane_color(PLOT_BACKGROUND_COLOR)
    ax.w_yaxis.set_pane_color(PLOT_BACKGROUND_COLOR)
    ax.w_zaxis.set_pane_color(PLOT_BACKGROUND_COLOR)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.grid(None)
    ax.view_init(elev=ELEV, azim=azimuth)
    plt.savefig(outfile, bbox_inches='tight')

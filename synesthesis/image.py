import os
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
BGD = '#212430'
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
import numpy as np
import scipy.signal as signal
from synesthesis.utils import atleast_kd


PLOT_BACKGROUND_COLOR = (33/255, 36/255, 48/255, 1)
COLOR = '#f7685d'
ALPHA = 0.4
ELEV = None
AZIM = 45
NUM_WIRES = 100


def _calc_stft(sampling_rate, sound_array, window_length, overlap_length):
    return signal.stft(sound_array, sampling_rate, axis=0, nperseg=window_length, noverlap=overlap_length)


def _transform_stft(stft):
    power_spectrum = np.abs(stft)**2
    return np.log(power_spectrum + 1)


def _smooth(array, smoothing_factor, window_length):
    sigma = smoothing_factor*window_length/100
    window = signal.get_window(('gaussian', sigma), window_length/2)
    window = window[:, None] * window[None, :]
    window = np.swapaxes(atleast_kd(window, array.ndim, append_dims=False), 0, 1)
    return signal.convolve(array, window, mode='same')


def _plot_spectrum(times, freqs, spectrum, outfile):
    X, Y = np.meshgrid(times, freqs)
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(X, Y, spectrum, color=COLOR, alpha=ALPHA, rcount=NUM_WIRES, ccount=NUM_WIRES)
    ax.w_xaxis.set_pane_color(PLOT_BACKGROUND_COLOR)
    ax.w_yaxis.set_pane_color(PLOT_BACKGROUND_COLOR)
    ax.w_zaxis.set_pane_color(PLOT_BACKGROUND_COLOR)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.grid(None)
    ax.view_init(elev=ELEV, azim=AZIM)
    plt.savefig(outfile, bbox_inches='tight', facecolor=PLOT_BACKGROUND_COLOR, edgecolor=PLOT_BACKGROUND_COLOR)


def save_image(sampling_rate, sound_array, window_length, overlap_length, smoothing_factor, outfile):
    times, freqs, stft = _calc_stft(sampling_rate, sound_array, window_length, overlap_length)

    scaled_spectrum = _transform_stft(stft.T)

    if smoothing_factor > 0:
        scaled_spectrum = _smooth(scaled_spectrum, smoothing_factor, window_length)

    try:
        _plot_spectrum(times, freqs, scaled_spectrum, outfile)
    except ValueError:
        for i in range(scaled_spectrum.shape[1]):
            outfile_name, ext = os.path.splitext(outfile)
            channel_outfile = outfile_name + f'_channel-{i}' + ext
            _plot_spectrum(times, freqs, scaled_spectrum[:, i, :], channel_outfile)

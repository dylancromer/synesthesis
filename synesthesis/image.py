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
from mpl_toolkits import mplot3d
import numpy as np
import scipy.signal as signal


PLOT_BACKGROUND_COLOR = (33/255, 36/255, 48/255, 1)
COLOR = '#f7685d'
ALPHA = 0.4
ELEV = 30
AZIM = 120


def _calc_stft(sampling_rate, sound_array, window_length, overlap_length):
    return signal.stft(sound_array, sampling_rate, axis=0, nperseg=window_length, noverlap=overlap_length)


def _transform_stft(stft):
    power_spectrum = np.abs(stft)**2
    return np.log(power_spectrum + 1)


def _smooth(array, smoothing_factor):
    sigma = smoothing_factor*window_length/100
    window = signal.get_window(('gaussian', sigma), window_length/2)
    return signal.convolve(transform, window, mode='same')


def _plot_spectrum(times, freqs, spectrum, outfile):
    X, Y = np.meshgrid(times, freqs)
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(X, Y, spectrum, color=COLOR, alpha=ALPHA)
    ax.view_init(elev=ELEV, azim=AZIM)
    ax.w_xaxis.set_pane_color(PLOT_BACKGROUND_COLOR)
    ax.w_yaxis.set_pane_color(PLOT_BACKGROUND_COLOR)
    ax.w_zaxis.set_pane_color(PLOT_BACKGROUND_COLOR)
    ax.grid(None)
    plt.savefig(outfile, bbox_inches='tight')


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

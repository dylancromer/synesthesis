import os
import numpy as np
import scipy.signal as signal
from synesthesis.utils import atleast_kd
import synesthesis.plotting
import synesthesis.animate


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


def save_image(sampling_rate, sound_array, window_length, overlap_length, smoothing_factor, azimuth, outfile):
    freqs, times, stft = _calc_stft(sampling_rate, sound_array, window_length, overlap_length)

    scaled_spectrum = _transform_stft(stft.T)

    if smoothing_factor > 0:
        scaled_spectrum = _smooth(scaled_spectrum, smoothing_factor, window_length)

    try:
        synesthesis.plotting.plot_spectrum(times, freqs, scaled_spectrum, azimuth,  outfile)
    except ValueError:
        for i in range(scaled_spectrum.shape[1]):
            outfile_name, ext = os.path.splitext(outfile)
            channel_outfile = outfile_name + f'_channel-{i}' + ext
            synesthesis.plotting.plot_spectrum(times, freqs, scaled_spectrum[:, i, :], azimuth, channel_outfile)


def save_animation(sampling_rate, sound_array, window_length, overlap_length, smoothing_factor, outfile):
    freqs, times, stft = _calc_stft(sampling_rate, sound_array, window_length, overlap_length)

    scaled_spectrum = _transform_stft(stft.T)

    if smoothing_factor > 0:
        scaled_spectrum = _smooth(scaled_spectrum, smoothing_factor, window_length)

    try:
        synesthesis.animate.animate_spectrum(times, freqs, scaled_spectrum, outfile)
    except ValueError:
        for i in range(scaled_spectrum.shape[1]):
            outfile_name, ext = os.path.splitext(outfile)
            channel_outfile = outfile_name + f'_channel-{i}' + ext
            synesthesis.animate.animate_spectrum(times, freqs, scaled_spectrum[:, i, :], channel_outfile)

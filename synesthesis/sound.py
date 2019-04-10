import time
import numpy as np
import sounddevice as sd
import scipy.signal as sig
from scipy.io import wavfile

def _calc_sound_and_framerate(image, duration):
    """Calculate the sound produced by the image, using an inverse short-time Fourier transform (ISTFT).

    Arguments:
    image -- array of image brightness values (2d numpy.ndarray)
    duration -- duration in seconds of the sound (float)

    returns tuple of ISTFT of image (np.ndarray), and framerate (float)
    """

    framerate = image.size/duration

    if image.shape[0] != image.shape[1]:
        time_axis = np.argmax(image.shape)
        freq_axis = np.argmin(image.shape)
    else:
        time_axis = 1
        freq_axis = 0

    image_stft = sig.istft(image, fs=framerate, time_axis=time_axis, freq_axis=freq_axis)[1] #istft returns time,amplitude pair

    return image_stft,framerate

def play_sound(image, duration):
    """Plays sound from image.

    Arguments:
    image -- array of image brightness values (2d numpy.ndarray)
    duration -- duration in seconds of the sound (float)
    """

    image_sound,framerate = _calc_sound_and_framerate(image, duration)

    sd.play(image_sound, framerate)
    time.sleep(duration)

def save_sound(image, duration, outfile):
    """Saves sound to specified output file.

    Arguments:
    image -- array of image brightness values (2d numpy.ndarray)
    duration -- duration in seconds of the sound (float)
    outfile -- location of output file for sound
    """
    image_sound,framerate = _calc_sound_and_framerate(image, duration)
    framerate = int(framerate)

    wavfile.write(outfile, framerate, image_sound)

import time
import numpy as np
import sounddevice as sd
import scipy.signal as sig
from scipy.io import wavfile

def _calc_sound_and_framerate(image, duration):
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
    image_inverted = 255 - image

    image_sound,framerate = _calc_sound_and_framerate(image_inverted, duration)

    print("Playing sound")
    sd.play(image_sound, framerate)
    time.sleep(duration)

def save_sound(image, duration, outfile):
    image_sound,framerate = _calc_sound_and_framerate(image, duration)

    wavfile.write(outfile, framerate, image_sound)

# synesthesis
*synes*thesia + syn*thesis*

Converts images to sound files with the sound power spectrum given by the image

## Basics
`synesthesis` is a command line program designed to create sounds which represent images, by interpretting the image as the short-time Fourier transform (STFT) of the sound. This allows you to see the image by recording it with a spectrogram.

Right now the math is about as basic as it gets. Ideally I would like to clean up the algorithm a bit to improve how the signal gets handled, but the program is usable as-is.

## Dependencies
`synesthesis` is written in Python 3, tested on version 3.7, and has several package dependencies:

- numpy
- scipy
- imageio
- sounddevice
- argparse

Indeed, much of the meat of this program is handled in these dependencies.

## Installation
The easiest way to install is with `pip`, by running

```pip install -e .```

in the directory containing `setup.py`. Alternatively you can run `setup.py` manually via

```python setup.py develop```

I highly recommend using either the `pip` `-e` flag (`--editable`), or installing with the `develop` option, as you can then pull new versions of the code without needing to reinstall.

## Usage
You can now run `synesthesis` via

```synesthesis [filename] [duration] [-i] [-o OUTFILE]```

`filename` is the input image location, and `duration` is the length of the sound you want to create. The `-i` flag inverts the brightness levels in the image optionally, and the `-o` optional argument takes an output file name (e.g. `output.wav`), redirecting the sound to a file instead of playing it.

## Troubleshooting
Please use the issues page to describe any problems or requests you encounter.

## Contributions
Pull requests welcome!

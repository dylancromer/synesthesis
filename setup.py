from distutils.core import setup
setup(name='synesthesis',
      version='0.1',
      py_modules=['synesthesis'],
      entry_points = {
          'console_scripts': [
              'synesthesis = synesthesis.main:main',
          ],
      },
)

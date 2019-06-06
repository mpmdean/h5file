from setuptools import setup

setup(name='h5file',
      version='0.1',
      description='Parser for files',
      url='http://github.com/mpmdean/h5file',
      author='Mark Dean',
      author_email='mdean@bnl.gov',
      packages=['h5file'],
      license='MIT',
      requires=['h5py', 're'],
      zip_safe=False)

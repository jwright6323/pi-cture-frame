# John C. Wright
# johnwright@eecs.berkeley.edu

from setuptools import setup

setup(name='pi-cture-frame',
      version='0.1',
      description='Raspberry Pi Picture Frame',
      url='http://github.com/jwright6323/pi-cture-frame',
      author='John C. Wright',
      author_email='johnwright@eecs.berkeley.edu',
      license='BSD',
      packages=['pi-cture-frame'],
      install_requires=[
          'flickrapi'
      ],
      zip_safe=False)

from setuptools import setup

setup(name='cryptochart',
      version='0.1',
      description='CLI tool to display cryptocurrency candlestick chart on Inky pHAT',
      url='http://github.com/storborg/funniest',
      author='Arnaud Durand',
      author_email='arnaud.durand@live.com',
      license='MIT',
      packages=['cryptochart'],
      install_requires=[
          'inkyphat',
          'Pillow',
          'matplotlib',
          'mplfinance>=0.12.5a3',
          'requests',
      ],
      entry_points={
          'console_scripts': ['cryptochart = cryptochart.cli:main'],
      },
      zip_safe=True)

from setuptools import setup

setup(name='cryptochart',
      version='0.2',
      description='CLI tool to display cryptocurrency candlestick chart on Inky pHAT',
      url='http://github.com/DurandA/inky-cryptochart',
      author='Arnaud Durand',
      author_email='arnaud.durand@live.com',
      license='MIT',
      packages=['cryptochart', 'cryptochart.fonts'],
      install_requires=[
          'Pillow',
          'matplotlib<3.6',
          'mplfinance>=0.12.5a3',
          'requests',
      ],
      extras_require={
        'inkyphat': ['inkyphat'],
        'inky': ['inky'],
        'waveshare_epd': ['waveshare_epd']
      },
      entry_points={
          'console_scripts': ['cryptochart = cryptochart.cli:main'],
      },
      package_data={
          'cryptochart': ['cryptochart/fonts/**'],
      },
      include_package_data=True,
      zip_safe=True)

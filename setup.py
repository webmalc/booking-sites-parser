"""The setup module for the booking-sites-parser"""
import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()
DESC = 'Parser for booking sites such as Booking.com, Homeaway, Airbnb'

setup(
    name='booking-sites-parser',
    version='0.0.2',
    description=DESC,
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/webmalc/booking-sites-parser',
    author='webmalc',
    author_email='m@webmalc.pw',
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.6.0',
    packages=find_packages(
        exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    include_package_data=True,
    install_requires=['requests', 'beautifulsoup4', 'fake-useragent'],
    entry_points={
        "console_scripts": [
            'booking-sites-parser=booking_sites_parser.__main__:run',
        ]
    },
)

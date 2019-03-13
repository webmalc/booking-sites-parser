# -*- coding: utf-8 -*-
"""The initialization module for the booking-sites-parser"""
from .models import Address, Property
from .parser import Parser

__all__ = ['Parser', 'Property', 'Address']
__author__ = "webmalc"
__version__ = "0.0.1"

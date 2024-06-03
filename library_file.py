from tkinter import *
from tkinter import font
import tkinter.ttk as ttk

import requests
import xml.etree.ElementTree as ET

import urllib.request
import urllib.parse

from PIL import Image, ImageTk
import io
from googlemaps import Client

favorites = []
client_id = "xFNxfdv0x0hZx61b5kW_"
client_secret = "62ROLhKEWc"
url = "https://openapi.naver.com/v1/search/image.xml?query="


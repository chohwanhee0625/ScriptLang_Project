from tkinter import *
from tkinter import font
import tkinter.ttk as ttk

import requests
import xml.etree.ElementTree as ET

from PIL import Image, ImageTk
import io
from googlemaps import Client

favorites = []

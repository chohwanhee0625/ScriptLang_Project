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

import telepot
import traceback
import sys

favorites = []
client_id = "xFNxfdv0x0hZx61b5kW_"
client_secret = "62ROLhKEWc"
url = "https://openapi.naver.com/v1/search/image.xml?query="

key = 'sea100UMmw23Xycs33F1EQnumONR%2F9ElxBLzkilU9Yr1oT4TrCot8Y2p0jyuJP72x9rG9D8CN5yuEs6AS2sAiw%3D%3D'
TOKEN = '7279986887:AAFoPg_7tTNxYZgu9VkNkDp9kGpGDJCJIgY'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)


def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)


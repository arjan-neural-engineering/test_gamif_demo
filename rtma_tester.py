# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 16:40:10 2022

@author: arjan
"""

import kivy
import pickle, math, threading, time, json, codecs, struct, random, ctypes, datetime, os, sys, shutil
import climber_config as md
import PyRTMA3 as PyRTMA
import numpy as np
from kivy.app import App
from PyRTMA3 import copy_to_msg, copy_from_msg
​
kivy.require('2.0.0')
​
sysConfig = md.loadLocalSysConfig()
MMM_IP = str(sysConfig["server"]) #"192.168.1.40:7111" (Chicago)  # "192.168.110.40:7111 (Pittsburgh)" #"localhost:7111 (DEBUG)"
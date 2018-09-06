#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 19:13:11 2018

@author: hu-tom
"""
import cv2
from Marker_Finder_Number import Finder_Number
img=cv2.imread('7.png')
imgp=Finder_Number(img,(6,7))  
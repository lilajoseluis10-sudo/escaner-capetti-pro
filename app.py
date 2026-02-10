import streamlit as st
import pytesseract
import cv2
import numpy as np
from PIL import Image

# Esto ayuda a que el sistema encuentre el camino de Tesseract en el servidor
import shutil
tesseract_path = shutil.which("tesseract")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

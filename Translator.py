from googletrans import Translator
from lxml import etree
import os

script_path = os.path.abspath(__file__)
script_path = os.path.dirname(script_path)
print(script_path)

translator = Translator()
translate = translator.translate
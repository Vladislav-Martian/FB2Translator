from googletrans import Translator
from lxml import etree
import os
import time

script_path = os.path.abspath(__file__)
script_path = os.path.dirname(script_path)


translator = Translator(service_urls=['translate.google.com'])

translate = translator.translate

print(translate("Hello", 'uk'))

FILES = [file for file in os.listdir(script_path) if file.endswith(".fb2")]

i = -1
for adr in FILES:
    i += 1
    FILES[i] = os.path.join(script_path, adr)
    
# List of files created.

LANG = "uk"
parser = etree.XMLParser()

FC = len(FILES)

print(f"Translating {FC} files")
j = 1
for adr in FILES:
    print(f"Translating file {j}:\n{adr}\n\n")
    xml_data = None
    with open(adr, 'rb') as file:
        xml_data = file.read()

    # Парсинг XML-структури файлу .fb2
    root = etree.fromstring(xml_data, parser)

    # Iterate through all XML elements
    for elem in root.getiterator():
        # Skip comments and processing instructions,
        # because they do not have names
        if not (
            isinstance(elem, etree._Comment)
            or isinstance(elem, etree._ProcessingInstruction)
        ):
            # Remove a namespace URI in the element's name
            elem.tag = etree.QName(elem).localname

    # Remove unused namespace declarations
    etree.cleanup_namespaces(root, None, None)

    paragraphs = root.xpath("//p")

    print(len(paragraphs), " Paragraphs\n")

    lim = -1 # for testing, set -1 on release
    counter = lim
    Number = len(paragraphs)
    for p in paragraphs:
        # time.sleep(1.5)
        if counter == 0:
            break
        translated_text = translator.translate(p.text, LANG, "ru")
        p.text = translated_text.text
        print(f"Text {Number}:", translated_text.text[:30], '...')
        Number -= 1
        counter -= 1

    filename = adr[:-4] + f" T({LANG})" + ".fb2"

    with open(filename, 'w', encoding="utf-8") as file:
        file.write(etree.tostring(root).decode("utf-8"))
import os

import pytesseract

from PIL import Image
from pdf2image import convert_from_path
import easyocr


# # Open PDF using pdf2image
# pages = convert_from_path('docs/SO/original/disk.pdf', 500)
#
# # Text extraction
# text = pytesseract.image_to_string(pages[0], lang='ita')
#
# # Print text
# print(text)


def text_from_image(path, lang='ita'):
    text = pytesseract.image_to_string(Image.open(path), lang=lang)
    return text


def text_from_pdf(path, lang='ita'):
    pages = convert_from_path(path, 300)
    text = []
    for page in pages:
        text.append(pytesseract.image_to_string(page, lang=lang))
    return text


class OCR:
    def __init__(self, lang='en'):
        self.reader = easyocr.Reader([lang])

    def text_from_image_gpu(self, path):
        text = self.reader.readtext(path, detail=0)
        return text

    def text_from_pdf_gpu(self, path):
        pages = convert_from_path(path, 250, fmt='jpeg')
        text = []
        batch_size = 1
        n_pages = len(pages)
        for i in range(0, n_pages, batch_size):
            out = self.reader.readtext_batched(pages[i:i + batch_size], detail=0)
            for page in out:
                text.append(' '.join(page))
        return text

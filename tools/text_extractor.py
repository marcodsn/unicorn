import os

import pytesseract

from PIL import Image
from pdf2image import convert_from_path


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


def split_text(text, delimiter='\n', remove_empty=True, max_len=750, merge=False):
    # If text is a list of strings (e.g. pages), merge them into a single string if merge=True
    if isinstance(text, list):
        if merge:
            text = delimiter.join(text)
            text = text.split(delimiter)
            if remove_empty:
                text = [line for line in text if line.strip() != '']
            for i in range(len(text)):
                if len(text[i]) > max_len:
                    # Get splitting point
                    split_point = text[i].find('. ', max_len)
                    # Split text
                    text.append(text[i][:split_point + 1])
                    text[i] = text[i][split_point + 2:]
                text[i] = text[i].strip()
        else:
            for page in text:
                page = page.split(delimiter)
                if remove_empty:
                    page = [line for line in page if line.strip() != '']
                for i in range(len(page)):
                    if len(page[i]) > max_len:
                        # Get splitting point
                        split_point = page[i].find('. ', max_len)
                        # Split text
                        page.append(page[i][:split_point + 1])
                        page[i] = page[i][split_point + 2:]
                    page[i] = page[i].strip()

    # If text is a single string, split it into a list of strings
    elif isinstance(text, str):
        text = text.split(delimiter)
        if remove_empty:
            text = [line for line in text if line.strip() != '']
        for i in range(len(text)):
            if len(text[i]) > max_len:
                # Get splitting point
                split_point = text[i].find('. ', max_len)
                # Split text
                text.append(text[i][:split_point + 1])
                text[i] = text[i][split_point + 2:]
            text[i] = text[i].strip()
    else:
        raise Exception('Text type not supported: {}; only list and string are supported'.format(type(text)))

    return text


def post_process(text):
    # Remove empty lines
    text = '\n'.join([line for line in text.split('\n') if line.strip() != ''])
    # Remove page numbers
    # text = '\n'.join([line for line in text.split('\n') if not line.strip().isdigit()])
    text = text.split('\n')
    return text


class Extractor:
    def __init__(self):
        pass

    def extract_text(self, path, split="page", lang='ita'):
        if path.endswith('.pdf'):
            pages = convert_from_path(path, 300)
            # text = pytesseract.image_to_string(pages[0], lang=self.lang)
            # Extract text from all pages
            if split == "page":
                text = []
                for page in pages:
                    text.append(pytesseract.image_to_string(page, lang=lang).replace('\n', ' ').replace('  ', ' '))
            elif split == "line":
                text = ''
                for page in pages:
                    text += pytesseract.image_to_string(page, lang=lang)
                    text += '\n'
                text = post_process(text)
            else:
                raise Exception('Split type not supported')

        elif path.endswith('.jpg'):
            text = pytesseract.image_to_string(Image.open(path), lang=lang)
        else:
            raise Exception('File format not supported')

        return text

    def extract_text_from_folder(self, path, split="page", lang='ita'):
        if split == "page":
            docs = []
            for file in os.listdir(path):
                texts = []
                if file.endswith('.pdf'):
                    pages = convert_from_path(file, 300)
                    for page in pages:
                        texts.append(pytesseract.image_to_string(page, lang=lang))
                elif file.endswith('.jpg') or file.endswith('.png'):
                    page = Image.open(file)
                    texts.append(pytesseract.image_to_string(page, lang=lang))
                else:
                    raise Exception('File type not supported: {}; only .pdf, .jpg and .png are supported'.format(file))
                docs.append(texts)

        elif split == "line":
            docs = ''
            for file in os.listdir(path):
                if file.endswith('.pdf'):
                    pages = convert_from_path(file, 300)
                    for page in pages:
                        docs += pytesseract.image_to_string(page, lang=self.lang)
                        docs += '\n'
                elif file.endswith('.jpg') or file.endswith('.png'):
                    page = Image.open(file)
                    docs += pytesseract.image_to_string(page, lang=self.lang)
                    docs += '\n'
                else:
                    raise Exception('File type not supported: {}; only .pdf, .jpg and .png are supported'.format(file))

        else:
            raise Exception('Split type not supported: {}; choose line or page'.format(split))


def extract_text(path, lang='ita'):
    text = []
    if path.endswith('.pdf'):
        pages = convert_from_path(path, 300)
        for page in pages:
            text.append(pytesseract.image_to_string(page, lang=lang).replace('\n', ' ').replace('  ', ' '))
    elif path.endswith('.jpg') or path.endswith('.png'):
        text.append(pytesseract.image_to_string(Image.open(path), lang=lang))
    else:
        raise Exception('File format not supported')
    return text


if __name__ == '__main__':
    file = 'docs/SO/original/disk.pdf'
    pages = text_from_pdf(file)
    print(pages[5])
    print("------------------")
    splitted = split_text(pages, merge=True, delimiter='. ')
    print(splitted[5])

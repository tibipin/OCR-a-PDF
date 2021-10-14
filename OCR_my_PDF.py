"""
Prerequisites:
==============
1. In order for this script to work, the Tesseract OCR tool for Windows needs to be installed.
The installer binary can be found here: https://github.com/UB-Mannheim/tesseract/wiki
2. After the installation, update the tesseract_executable_path with the path to the tesseract executable
"""

import os
from pikepdf import Pdf, PdfImage
from concurrent.futures import ThreadPoolExecutor
import pytesseract

tesseract_executable_path = fr"{os.environ['LOCALAPPDATA']}\Programs\Tesseract-OCR\tesseract.exe"


class NonEditablePDF:
    """
    Takes as an input a non-editable PDF path and OCRs it
    =====================================================


    Attributes:
        pdf_structure : dict -> of the format {pdf page number: images on page}
        text_from_pdf : str -> text after OCR has been performed on all images of the PDF

    Methods:
        __init__:
            file_name : str -> path to PDF file
            compression_level: int (btw 0 and 1) -> high compression level = longer OCR time, higher text precision
                                                 -> low compression level = faster OCR time, lower text precision
            tesseract_exe: path to tesseract executable
        export_txt_file(): Exports the OCRed text from the pdf to a text file with the same name as the pdf
    """

    def __init__(self, file_name, compression_level=0.5, tesseract_exe=tesseract_executable_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_exe
        self._file = file_name
        pdf_file = Pdf.open(self._file)
        pages = [page_no for page_no in range(len(pdf_file.pages))]
        images = [list(pdf_file.pages[page_no].images) for page_no in pages]
        self.pdf_structure = dict(zip(pages, images))
        pdf_images = [PdfImage(pdf_file.pages[page_no].images[raw_image]).as_pil_image()
                      for page_no in self.pdf_structure
                      for raw_image in self.pdf_structure[page_no]
                      if self.pdf_structure[page_no]]
        resized_pdf_images = [i.resize([int(compression_level * s) for s in i.size]) for i in pdf_images]
        with ThreadPoolExecutor() as tp_executor:
            text_results = tp_executor.map(pytesseract.image_to_string, resized_pdf_images)
        self.text_from_pdf = ''.join(text_results)

    def export_txt_file(self):
        f = open(f'{self._file[:-4]}.txt', 'w')
        f.write(self.text_from_pdf)
        f.close()

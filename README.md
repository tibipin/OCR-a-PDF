# OCR my PDF

#### Short python script used to OCR pdfs

---
#### Prerequisites:
1. In order for this script to work, the Tesseract OCR tool for Windows needs to be installed.
The installer binary can be found [here](https://github.com/UB-Mannheim/tesseract/wiki)
2. After the installation, update the `tesseract_executable_path` variable with the path to the tesseract executable
---
#### Quick usage:

Read a PDF

`mypdf = NonEditablePDF(non_editable_pdf_file_path)`

Export it as a text file

`mypdf.export_txt_file()`

---

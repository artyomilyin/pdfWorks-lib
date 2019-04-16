## pdfWorks-lib

pdfWorks-lib is a small tool written on `python` using `img2pdf` and `PyPDF2` libraries.

There are two methods that allow you to merge images and PDF files into one
or split your PDF file page by page:

### convert()
Convert is a tool that combines both converting images to PDF files (considering orientation) 
and merging all the gathered files into one single PDF document.

Example of usage:
```
from pdfworks_lib.pdfworks import Converter

converter = Converter()
input_files = ['~/file1.jpg', '~/file2.png', '~/file3.pdf']
output_file = '~/output.pdf'
converter.convert(input_files, output_file)
```

### split()
Split is a tool that can split your PDF document page by page into selected directory.

Example of usage:
```
from pdfworks_lib.pdfworks import Converter

converter = Converter()
input_file = '~/file.pdf'
output_dir = '~/output_directory/'
converter.convert(input_file, output_dir)
```
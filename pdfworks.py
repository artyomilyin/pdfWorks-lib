import os
import shutil
import ntpath
import sys
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
from PIL import Image
import img2pdf


class Converter:
    SUPPORTED_IMAGE_FILE_FORMATS = ['.jpg', '.jpeg', '.png']

    def convert(self, input_files_list, output_filename):

        if not os.path.exists(self.tempdir):
            os.makedirs(self.tempdir)

        for file in input_files_list:
            if file.lower().endswith(tuple(self.SUPPORTED_IMAGE_FILE_FORMATS)):
                new_filename = os.path.join(self.tempdir, ntpath.split(file)[1] + '.pdf')

                with Image.open(file) as image_file:
                    x, y = image_file.size
                    if x > y:
                        this_layout = self.layout_fun_horizontal
                    else:
                        this_layout = self.layout_fun_vertical

                with open(file, 'rb') as r, open(new_filename, 'wb') as w:
                    try:
                        w.write(img2pdf.convert(r, layout_fun=this_layout))
                    except TypeError as e:
                        print(e)
                self.FINAL_LIST.add(new_filename)

            if file.endswith('.pdf'):
                self.FINAL_LIST.add(file)

        merger = PdfFileMerger(strict=False)

        for file in sorted(list(self.FINAL_LIST)):
            self.FILE_HANDLES.append(open(file, 'rb'))
            merger.append(self.FILE_HANDLES[-1])

        with open(output_filename, 'wb') as w:
            merger.write(w)

        for handle in self.FILE_HANDLES:
            handle.close()

        self.FINAL_LIST = set()

        shutil.rmtree(self.tempdir, ignore_errors=True)

    @staticmethod
    def split_pdf(filename, folder):
        with open(filename, 'rb') as infile:
            reader = PdfFileReader(infile, strict=False)
            for i in range(1, reader.numPages + 1):
                writer = PdfFileWriter()
                writer.addPage(reader.getPage(i - 1))
                outfile_name = os.path.join(
                    folder,
                    os.path.splitext(ntpath.split(filename)[1])[0] + '_' + str(i) + '.pdf'
                )
                print(outfile_name)
                with open(outfile_name, 'wb') as outfile:
                    writer.write(outfile)

    def __init__(self):
        self.input_files = None
        self.layout_fun_vertical = img2pdf.get_layout_fun((img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297)))
        self.layout_fun_horizontal = img2pdf.get_layout_fun((img2pdf.mm_to_pt(297), img2pdf.mm_to_pt(210)))
        self.FILE_HANDLES = []
        self.FINAL_LIST = set()
        self.INPUT_LIST = []
        self.homedir = os.path.expanduser('~')

        if sys.platform == 'win32':
            self.tempdir = os.sep.join([self.homedir, 'Application Data', 'pdfWorks'])
        else:
            self.tempdir = os.sep.join([self.homedir, '.pdfWorks'])

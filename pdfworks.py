#test1
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
import img2pdf
import os
import shutil
import ntpath
import sys
from datetime import datetime


class Converter:

    SUPPORTED_IMAGE_FILE_FORMATS = ['.jpg', '.png']

    def files_chosen(self):
        if self.input_files is not None:
            return True
        else:
            return False

    def set_input_files(self, files_list):

        if not os.path.exists(self.tempdir):
            os.makedirs(self.tempdir)

        for file in files_list:
            if file.lower().endswith(tuple(self.SUPPORTED_IMAGE_FILE_FORMATS)):
                new_filename = os.path.join(self.tempdir, ntpath.split(file)[1]+'.pdf')
                with open(file, 'rb') as r, open(new_filename, 'wb') as w:
                    try:
                        w.write(img2pdf.convert(r, layout_fun=self.layout_fun))
                    except TypeError as e:
                        print(e)
                self.FINAL_LIST.add(new_filename)

            if file.endswith('.pdf'):
                self.FINAL_LIST.add(file)

    def convert(self, filename):

        merger = PdfFileMerger()

        for file in sorted(list(self.FINAL_LIST)):
            self.FILE_HANDLES.append(open(file, 'rb'))
            merger.append(self.FILE_HANDLES[-1])

        with open(filename, 'wb') as w:
            merger.write(w)

        for handle in self.FILE_HANDLES:
            handle.close()

        self.FINAL_LIST = set()

        shutil.rmtree(self.tempdir, ignore_errors=True)

    def split(self, filename, folder):

        with open(filename, 'rb') as infile:

            reader = PdfFileReader(infile)
            for i in range(1, reader.numPages+1):
                writer = PdfFileWriter()
                writer.addPage(reader.getPage(i-1))
                outfile_name = os.path.join(
                    folder,
                    os.path.splitext(ntpath.split(filename)[1])[0] + '_' + str(i) + '.pdf'
                )
                print(outfile_name)
                with open(outfile_name, 'wb') as outfile:
                    writer.write(outfile)

    def __init__(self):
        self.input_files = None
        self.a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
        self.layout_fun = img2pdf.get_layout_fun(self.a4inpt)
        self.FILE_HANDLES = []
        self.FINAL_LIST = set()
        self.INPUT_LIST = []
        self.homedir = os.path.expanduser('~')

        if sys.platform == 'win32':
            self.tempdir = os.sep.join([self.homedir, 'Application Data', 'pdfWorks'])
        else:
            self.tempdir = os.sep.join([self.homedir, '.pdfWorks'])


if __name__ == '__main__':
    Converter().convert('OUTPUT/'+datetime.strftime(datetime.now(), '%Y%B%d_%H%M%S')+'.pdf')


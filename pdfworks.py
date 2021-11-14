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
        """
        :param input_files_list: list of full paths to files to be converted and merged
        :param output_filename: output filename
        """

        # check if temporary dir exists
        if not os.path.exists(self.tempdir):
            os.makedirs(self.tempdir)

        for file in input_files_list:
            # consider only image files that are supported
            if file.lower().endswith(tuple(self.SUPPORTED_IMAGE_FILE_FORMATS)):
                # convert image to pdf
                new_filename = os.path.join(self.tempdir, ntpath.split(file)[1] + '.pdf')

                # consider image orientation
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
                self.FINAL_LIST.append(new_filename)

            if file.lower().endswith('.pdf'):
                # if file is pdf than just add it to the list
                self.FINAL_LIST.append(file)

        if self.FINAL_LIST:
            # add file by file to the output pdf document
            merger = PdfFileMerger(strict=False)
            for file in self.FINAL_LIST:
                self.FILE_HANDLES.append(open(file, 'rb'))
                merger.append(self.FILE_HANDLES[-1])

            with open(output_filename, 'wb') as w:
                merger.write(w)

            for handle in self.FILE_HANDLES:
                handle.close()

            self.FINAL_LIST = set()
        else:
            print("nothing to merge")
        # clean temporary directory
        shutil.rmtree(self.tempdir, ignore_errors=True)

    @staticmethod
    def split_pdf(filename, folder):
        """
        :param filename: full path to the file to be splitted
        :param folder: directory in which output files are to be put
        """
        with open(filename, 'rb') as infile:
            reader = PdfFileReader(infile, strict=False)
            for i in range(1, reader.numPages + 1):
                writer = PdfFileWriter()
                writer.addPage(reader.getPage(i - 1))
                outfile_name = os.path.join(
                    folder,
                    os.path.splitext(ntpath.split(filename)[1])[0] + '_' + str(i) + '.pdf'
                )
                with open(outfile_name, 'wb') as outfile:
                    writer.write(outfile)

    def __init__(self):
        self.input_files = None
        self.layout_fun_vertical = img2pdf.get_layout_fun((img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297)))
        self.layout_fun_horizontal = img2pdf.get_layout_fun((img2pdf.mm_to_pt(297), img2pdf.mm_to_pt(210)))
        self.FILE_HANDLES = []
        self.FINAL_LIST = []
        self.INPUT_LIST = []
        self.homedir = os.path.expanduser('~')

        # define temporary directory location
        if sys.platform == 'win32':
            self.tempdir = os.sep.join([self.homedir, 'Application Data', 'pdfWorks'])
        else:
            self.tempdir = os.sep.join([self.homedir, '.pdfWorks'])

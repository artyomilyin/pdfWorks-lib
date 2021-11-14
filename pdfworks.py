import os
import shutil
import ntpath
import sys
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
from PIL import Image
import img2pdf


LAYOUT_FUNC_VERTICAL = img2pdf.get_layout_fun((img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297)))
LAYOUT_FUNC_HORIZONTAL = img2pdf.get_layout_fun((img2pdf.mm_to_pt(297), img2pdf.mm_to_pt(210)))


class Converter:
    SUPPORTED_IMAGE_FILE_FORMATS = ['.jpg', '.jpeg', '.png']

    def _define_image_layout(self, filename):
        with Image.open(filename) as image_file:
            x, y = image_file.size
            layout_func = LAYOUT_FUNC_HORIZONTAL if x > y else LAYOUT_FUNC_VERTICAL
            return layout_func

    def _convert_to_temporary_pdf(self, filename, new_filename):
        layout_func = self._define_image_layout(filename)
        with open(filename, 'rb') as r, open(new_filename, 'wb') as w:
            try:
                w.write(img2pdf.convert(r, layout_fun=layout_func))
            except TypeError as e:
                print(e)

    def convert(self, input_files_list, output_filename):
        """
        :param input_files_list: list of full paths to files to be converted and merged
        :param output_filename: output filename
        """

        # check if temporary dir exists
        if not os.path.exists(self.tempdir):
            os.makedirs(self.tempdir)

        input_pdf_list = []
        for file in input_files_list:
            # consider only image files that are supported
            if file.lower().endswith(tuple(self.SUPPORTED_IMAGE_FILE_FORMATS)):
                # convert image to pdf
                new_filename = os.path.join(self.tempdir, ntpath.split(file)[1] + '.pdf')

                # consider image orientation
                self._convert_to_temporary_pdf(file, new_filename)
                input_pdf_list.append(new_filename)

            if file.lower().endswith('.pdf'):
                # if file is pdf than just add it to the list
                input_pdf_list.append(file)

        if input_pdf_list:
            # add file by file to the output pdf document
            merger = PdfFileMerger(strict=False)
            file_handles = []
            for file in input_pdf_list:
                file_handles.append(open(file, 'rb'))
                merger.append(file_handles[-1])

            with open(output_filename, 'wb') as w:
                merger.write(w)

            for handle in file_handles:
                handle.close()
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
        # define temporary directory location
        homedir = os.path.expanduser('~')
        if sys.platform == 'win32':
            self.tempdir = os.sep.join([homedir, 'Application Data', 'pdfWorks'])
        else:
            self.tempdir = os.sep.join([homedir, '.pdfWorks'])

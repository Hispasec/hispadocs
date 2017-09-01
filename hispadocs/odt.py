# coding=utf-8
import os
import tempfile
import zipfile

from lxml import etree
from ooopy import Transforms as Transforms
from ooopy.OOoPy import OOoPy
from ooopy.Transformer import Transformer

CONTENT_FILENAME = 'content.xml'

class OdtFiles(list):
    def __init__(self, files):
        super(OdtFiles, self).__init__(files)

    def create_output(self, output_path):
        o = OOoPy(infile=self[0], outfile=output_path)
        if len(self) > 1:
            t = Transformer(
                o.mimetype,
                Transforms.get_meta(o.mimetype),
                Transforms.Concatenate(*(self[1:])),
                Transforms.renumber_all(o.mimetype),
                Transforms.set_meta(o.mimetype),
                Transforms.Fix_OOo_Tag(),
                Transforms.Manifest_Append()
            )
            t.transform(o)
        o.close()


class OdtFile(object):
    def __init__(self, path):
        self.path = path

    def get_zip_data(self, path=None):
        return zipfile.ZipFile(path or self.path)

    def unzip(self):
        # Directorio al que se extraerá
        directory = tempfile.gettempdir()
        zipdata = self.get_zip_data()
        zipdata.extractall(directory)
        return directory, zipdata

    def zip(self, directory, output=None):
        output = output or self.path
        zipinfos = self.get_zip_data().infolist()
        with zipfile.ZipFile(output, 'w') as outzip:
            for zipinfo in zipinfos:
                file_name = zipinfo.filename  # The name and path as stored in the archive
                file_url = os.path.join(directory, file_name)  # The actual name and path
                outzip.write(file_url, file_name)

    def replace_zip(self, zipdata, directory, output):
        """Reemplazar un contenido de zip por el de una carpeta. Esto se hace
        así para conservar el orden de los archivos. Odt requiere que el orden
        sea el mismo.
        :param zipdata: una instancia ZipFile. Usado para conservar el orden de archivos
        :param directory: El directorio del que se obtendrán los archivos a reemplazar
        :param output: El nuevo archivo que se generará
        :return:
        """
        with zipfile.ZipFile(output, 'w') as outzip:
            zipinfos = zipdata.infolist()
            for zipinfo in zipinfos:
                file_name = zipinfo.filename  # The name and path as stored in the archive
                file_url = os.path.join(directory, file_name)  # The actual name and path
                outzip.write(file_url, file_name)

    def read_odt_file(self, filename):
        directory, zipdata = self.unzip()
        content_path = os.path.join(directory, filename)
        # TODO: borrar zip
        return open(content_path).read()

    def read_content(self):
        return self.read_odt_file(CONTENT_FILENAME)

    def write_odt_file(self, filename, body):
        directory, zipdata = self.unzip()
        content_path = os.path.join(directory, filename)
        with open(content_path, 'w') as f:
            f.write(body)
        self.zip(directory)

    def write_content(self, body):
        return self.write_odt_file(CONTENT_FILENAME, body)

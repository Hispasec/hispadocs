# coding=utf-8
import os
import tempfile
import zipfile
from lxml import etree


CONTENT_FILENAME = 'content.xml'
TEXT_NAMESPACE = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'

class OdtReplace(object):
    def __init__(self, path, variables):
        self.path = path
        self.variables = variables

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

    def replace_dir_content(self, directory):
        content_path = os.path.join(directory, CONTENT_FILENAME)
        root = etree.parse(open(content_path)).getroot()
        nodes = root.findall(".//{%s}*" % TEXT_NAMESPACE)
        for node in nodes:
            if node.text is None:
                continue
            node.text = node.text.format(**self.variables)
        out = etree.tostring(root)
        with open(content_path, 'w') as f:
            f.write(out)

    def replace(self):
        directory, zipdata = self.unzip()
        self.replace_dir_content(directory)
        self.zip(directory)

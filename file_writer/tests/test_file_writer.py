import os

from file_writer import NexusFileWriter, NeXusFileXMLWriter


def test_nexus_file_xml_writer():
    file_writer = NeXusFileXMLWriter()
    file_writer.configure(layout_file=os.path.abspath("./layout_cSAXS_NXsas.xml"))
    file_writer.write("./test.h5", {})


def test_nexus_file_writer():
    file_writer = NexusFileWriter()
    file_writer.write("./test.h5", {})

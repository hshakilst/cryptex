#!/usr/bin/python
from pdfrw import PdfReader, PdfWriter
from docx import Document
import pyexiv2
import magic
from module import crypto
import umsgpack
from file_metadata.generic_file import GenericFile
import ast
import json

# keywords are json objects


def add_pdf_keyword(fname, keyword):
    trailer = PdfReader(fname)
    keys = str(keyword)
    trailer.Info.Keywords = keys
    PdfWriter(fname, trailer=trailer).write()
    return True


def read_pdf_keyword(fname):
    trailer = PdfReader(fname)
    keys = ast.literal_eval(trailer.Info.Keywords)
    return keys


def add_doc_keyword(fname, keyword):
    document = Document(fname)
    core_properties = document.core_properties
    keys = str(keyword)
    core_properties.keywords = keys
    document.save(fname)
    return True


def read_doc_keyword(fname):
    document = Document(fname)
    core_properties = document.core_properties
    keys = ast.literal_eval(core_properties.keywords)
    return keys


def add_img_keyword(fname, keyword):
    metadata = pyexiv2.ImageMetadata(fname)
    metadata.read()
    key = 'Exif.Image.ImageDescription'
    keys = str(keyword)
    metadata[key] = keys
    metadata.write()
    return True


def read_img_keyword(fname):
    metadata = pyexiv2.ImageMetadata(fname)
    metadata.read()
    key = 'Exif.Image.ImageDescription'
    keys = ast.literal_eval(metadata[key])
    return keys


def detect_file_type(fname, operation, keyword):
    file_type = magic.from_file(fname, mime="true")
    if(file_type == 'application/pdf'):
        if(operation == 'write'):
            flag = add_pdf_keyword(fname, keyword)
            if(flag):
                print "Metdata write successful!"
        elif(operation == 'read'):
            keys = read_pdf_keyword(fname)
            return keys
    elif(file_type == 'image/jpeg'):
        if(operation == 'write'):
            flag = add_img_keyword(fname, keyword)
            if(flag):
                print "Metdata write successful!"
        elif(operation == 'read'):
            keys = read_img_keyword(fname)
            return keys
    elif (file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
        if(operation == 'write'):
            flag = add_doc_keyword(fname, keyword)
            if(flag):
                print "Metdata write successful!"
        elif(operation == 'read'):
            keys = read_doc_keyword(fname)
            return keys
    elif (file_type == 'text/plain' and fname.lower().endswith('.enc')):
        if (operation == 'write'):
            print "Can't write to a encrypted file!"
        else:
            file = GenericFile.create(fname)
            res = json.dumps(file.analyze(), sort_keys=True, indent=4)
            print res
    else:
        if(file_type == 'application/octet-stream'):
            if(operation == 'write'):
                flag = add_doc_keyword(fname, keyword)
                if(flag):
                    print "Metdata write successful!"
            elif(operation == 'read'):
                keys = read_doc_keyword(fname)
                return keys
        else:
            print 'I can\'t handle this type of file yet!'


def add_keywords(fname, properties):
    return detect_file_type(fname, 'write', properties)


def read_keywords(fname):
    return detect_file_type(fname, 'read', {})

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip
import logging
import os
import shutil
import zipfile

import tensorflow as tf


def extract(filename, files=None):
  extension = os.path.splitext(filename)[1][1:]
  if extension == 'zip':
    return extract_zip(filename, files)
  if extension == 'gz':
    assert not files or files == (os.path.splitext(files[0])[0],)
    return extract_gz(filename)
  raise NotImplementedError()


def extract_zip(filename, files=None):
  directory = os.path.dirname(filename)
  with tf.gfile.FastGFile(filename, 'rb') as archive_file:
    with zipfile.ZipFile(archive_file) as archive:
      if not files:
        files = sorted(archive.namelist())
      destinations = tuple(os.path.join(directory, name) for name in files)
      for name, destination in zip(files, destinations):
        if tf.gfile.Exists(destination):
          logging.info("Skip existing '{}'.".format(destination))
          continue
        logging.info("Extract '{}'.".format(destination))
        with tf.gfile.FastGFile(destination, 'w') as output_file:
          output_file.write(archive.read(name))
      return destinations


def extract_gz(filename):
  destination = os.path.splitext(filename)[0]
  if tf.gfile.Exists(destination):
    logging.info("Skip existing '{}'.".format(destination))
    return destination
  with tf.gfile.FastGFile(filename, 'rb') as archive_file:
    with gzip.GzipFile(fileobj=archive_file) as archive:
      with tf.gfile.FastGFile(destination, 'wb') as target:
        shutil.copyfileobj(archive, target)
  return destination

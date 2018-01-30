from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from six.moves.urllib import request
import logging
import os
import shutil

import tensorflow as tf


def download(directory, url):
  directory = os.path.expanduser(directory)
  tf.gfile.MakeDirs(directory)
  filename = os.path.join(directory, os.path.split(url)[1])
  if tf.gfile.Exists(filename):
    logging.info("Skip existing '{}'.".format(filename))
  else:
    logging.info("Download '{}'.".format(filename))
    stream = request.urlopen(url)
    with tf.gfile.FastGFile(filename, 'wb') as file_:
      shutil.copyfileobj(stream, file_)
  return filename

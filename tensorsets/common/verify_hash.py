from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib
import logging

import tensorflow as tf


def verify_hash(filename, md5=None, sha1=None, sha256=None):
  hashes = (hashlib.md5(), hashlib.sha1(), hashlib.sha256())
  with tf.gfile.FastGFile(filename, 'rb') as file_:
    content = True
    while content:
      content = file_.read(8192)
      for hash_ in hashes:
        hash_.update(content)
  hashes = tuple(hash_.hexdigest() for hash_ in hashes)
  references = (md5, sha1, sha256)
  logging.info("Verifying hashes of '{}'.".format(filename))
  if any(rhs and lhs != rhs for lhs, rhs in zip(hashes, references)):
    message = "Invalid hash. Please delete or manually provide '{}'."
    raise Exception(message.format(filename))

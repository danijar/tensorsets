from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf


def count_batches(dataset):
  iterator = dataset.make_initializable_iterator()
  batch = iterator.get_next()
  with tf.Session() as sess:
    sess.run(iterator.initializer)
    count = 0
    try:
      while True:
        sess.run(batch)
        count += 1
    except tf.errors.OutOfRangeError:
      pass
  return count


def compute_value_range(dataset):
  iterator = dataset.make_initializable_iterator()
  batch = iterator.get_next()
  min_, max_ = np.inf, -np.inf
  with tf.Session() as sess:
    sess.run(iterator.initializer)
    try:
      while True:
        current = sess.run(batch)
        min_ = min(min_, current.min())
        max_ = max(max_, current.max())
    except tf.errors.OutOfRangeError:
      pass
  return min_, max_


def read_records(dataset, amount):
  iterator = dataset.make_initializable_iterator()
  batch = iterator.get_next()
  records = []
  with tf.Session() as sess:
    sess.run(iterator.initializer)
    for _ in range(amount):
      records.append(sess.run(batch))
  return records

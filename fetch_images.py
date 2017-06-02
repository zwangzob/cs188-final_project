"""Modified Olivetti faces dataset.

The original database was available from

    http://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html

The version retrieved here comes in MATLAB format from the personal
web page of Sam Roweis:

    http://www.cs.nyu.edu/~roweis/

There are ten different images of each of 40 distinct subjects. For some
subjects, the images were taken at different times, varying the lighting,
facial expressions (open / closed eyes, smiling / not smiling) and facial
details (glasses / no glasses). All the images were taken against a dark
homogeneous background with the subjects in an upright, frontal position (with
tolerance for some side movement).

The original dataset consisted of 92 x 112, while the Roweis version
consists of 64x64 images.
"""
# Copyright (c) 2011 David Warde-Farley <wardefar at iro dot umontreal dot ca>
# License: BSD 3 clause

from io import BytesIO
from os.path import exists
from os import makedirs
try:
    # Python 2
    import urllib2
    urlopen = urllib2.urlopen
except ImportError:
    # Python 3
    import urllib.request
    urlopen = urllib.request.urlopen

import numpy as np
from scipy.io.matlab import loadmat

from .base import get_data_home, Bunch
from .base import _pkl_filepath
from ..utils import check_random_state
from ..externals import joblib

# add our library
from img2array import img2array_converter

DATA_URL = "http://cs.nyu.edu/~roweis/data/olivettifaces.mat"
TARGET_FILENAME = "angiograms.pkz"

# Grab the module-level docstring to use as a description of the
# dataset
MODULE_DOCS = __doc__


def fetch_angiogram_images(data_home=None, shuffle=False, random_state=0,
                         download_if_missing=True):
    data_home = get_data_home(data_home=data_home)
    if not exists(data_home):
        makedirs(data_home)
    filepath = _pkl_filepath(data_home, TARGET_FILENAME)
    if not exists(filepath):
        # print('downloading Olivetti faces from %s to %s'
        #      % (DATA_URL, data_home))
        # fhandle = urlopen(DATA_URL)
        # buf = BytesIO(fhandle.read())
        # mfile = loadmat(buf)
        # faces = mfile['faces'].T.copy()
	faces = img2array_converter()_
        joblib.dump(faces, filepath, compress=6)
        #del mfile
    else:
        faces = joblib.load(filepath)
    # We want floating point data, but float32 is enough (there is only
    # one byte of precision in the original uint8s anyway)
    faces = np.float32(faces)
    faces = faces - faces.min()
    faces /= faces.max()
    faces = faces.reshape((400, 64, 64)).transpose(0, 2, 1)
    # 10 images per class, 400 images total, each class is contiguous.
    target = np.array([i // 10 for i in range(400)])
    if shuffle:
        random_state = check_random_state(random_state)
        order = random_state.permutation(len(faces))
        faces = faces[order]
        target = target[order]
    return Bunch(data=faces.reshape(len(faces), -1),
                 images=faces,
                 target=target,
                 DESCR=MODULE_DOCS)

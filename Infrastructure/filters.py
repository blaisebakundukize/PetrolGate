#!/usr/bin/env python2
#

import re
import hashlib
import string
import mimetypes


def add_hash(path):
    """Generates a hash from a file.

    Args:
      path: (string) The path to the file to generate the hash from.

    Returns:
      Returns a hash digest (string) of the file.
    """
    blocksize = 32768
    file_hash = hashlib.sha256()
    file_path = re.sub(r'/bon/', './', path)

    with open(file_path) as file_to_hash:
        file_buffer = file_to_hash.read(blocksize)
        while (len(file_buffer) > 0):
            file_hash.update(file_buffer)
            file_buffer = file_to_hash.read(blocksize)

    return re.sub(r'(.*?)\.(.*)$', ("\\1.%s.\\2" % file_hash.hexdigest()), path)

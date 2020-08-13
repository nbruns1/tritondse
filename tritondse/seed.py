#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib


class Seed(object):
    """
    This class is used to represent a seed input. The seed will be injected
    into stdin or argv according to the Triton DSE configuration.
    """
    def __init__(self, content = bytes()):
        self.content = bytes(content)


    def get_size(self):
        """
        Returns the size of the seed.
        """
        return len(self.content)


    def get_hash(self):
        """
        Returns the md5 hash of the content
        """
        m = hashlib.md5(self.content)
        return m.hexdigest()

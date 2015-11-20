#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_captainwebhook
----------------------------------

Tests for `captainwebhook` module.
"""

import unittest
from collections import namedtuple

from captainwebhook.captainwebhook import get_handler, BaseHTTPRequestHandler


class TestCaptainwebhook(unittest.TestCase):

    def test_something(self):
        args = namedtuple("Args", ["key", "command"])("some key", "some command")
        PullHandler = get_handler(args)
        self.assertTrue(issubclass(PullHandler, BaseHTTPRequestHandler))

if __name__ == '__main__':
    unittest.main()

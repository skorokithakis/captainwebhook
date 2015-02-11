#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_captainwebhook
----------------------------------

Tests for `captainwebhook` module.
"""

import unittest

from captainwebhook.captainwebhook import get_handler, BaseHTTPRequestHandler


class TestCaptainwebhook(unittest.TestCase):

    def test_something(self):
        PullHandler = get_handler("some key", "echo hi")
        self.assertTrue(issubclass(PullHandler, BaseHTTPRequestHandler))

if __name__ == '__main__':
    unittest.main()

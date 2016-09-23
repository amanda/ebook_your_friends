#!usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from markov import fix_apostrophes, fix_nt, fix_tco, fix_hashtags, fix_therest, final_cleanup


class TestCleanup(unittest.TestCase):

    def test_apostrophes(self):
        s1 = "my sister 's dog"
        s2 = "her friend 's sister 's dog"
        s3 = "my roommate 's dress"
        self.assertEqual("my sister's dog", fix_apostrophes(s1))
        self.assertEqual("her friend's sister's dog", fix_apostrophes(s2))
        self.assertEqual("my roommate's dress", fix_apostrophes(s3))

    def test_nt(self):
        s1 = "do n't do that"
        s2 = "that is n't cool"
        s3 = "that does n't work"
        s4 = "n't hear what that horse is very well done check it's first php function has pledged to diff-so-fancy."
        self.assertEqual("don't do that", fix_nt(s1))
        self.assertEqual("that isn't cool", fix_nt(s2))
        self.assertEqual("that doesn't work", fix_nt(s3))
        self.assertEqual("hear what that horse is very well done check it's first php function has pledged to diff-so-fancy.", fix_nt(s4))

    def test_tco(self):
        s1 = "cool tweet here //t.co/djskadhla yep"
        s2 = "//t.co/"
        self.assertEqual("cool tweet here yep", fix_hashtags(s1))
        self.assertEqual("", fix_hashtags(s2))

    def test_hashtags(self):
        s1 = "#"
        s2 = "# whatever"
        self.assertEqual("", fix_hashtags(s1))
        self.assertEqual("", fix_hashtags(s2))

    def test_nna(self):
        s1 = "gon na be awesome"
        self.assertEqual("gonna be awesome", fix_therest(s1))

    def test_quotes(self):
        s1 = "hey cool “”“ what no"
        self.assertEqual("hey cool what no", fix_therest(s1))

    def test_ellipses(self):
        s1 = "nope ... ... what"
        s2 = "hey ... what"
        self.assertEqual("nope...what", fix_therest(s1))
        self.assertEqual("hey...what", fix_therest(s2))

    def test_final_cleanup(self):
        s1 = "nope ... what # whatever do n't do “”“ that.."
        s2 = "gon na be //t.co/ good if.."
        self.assertEqual(
            "nope...what whatever don't do that.", final_cleanup(s1))
        self.assertEqual("gonna be good if.", final_cleanup(s2))

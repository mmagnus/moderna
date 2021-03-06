#!/usr/bin/env python

from moderna.sequence.AlignmentMatcher import AlignmentMatcher
from moderna.sequence.RNAAlignment import read_alignment
from moderna.sequence.ModernaSequence import Sequence
from tests.test_data import *
from unittest import TestCase, main

class AlignmentMatcherTests(TestCase):
    
    def setUp(self):
        self.ali = read_alignment(MINI_ALIGNMENT)
        self.template_seq = Sequence("GCGGAUUUALCUCAG")
        self.target_seq = Sequence("ACUGUGAYUA[UACCU#PG")
    
    def test_init(self):
        """Initializing Matcher"""
        a = AlignmentMatcher(self.ali)
        self.assertEqual(a.align, self.ali)
        
    def test_is_target_identical(self):
        """Compare template and target"""
        a = AlignmentMatcher(self.ali)
        self.assertTrue(a.is_target_identical(self.target_seq))
        self.assertFalse(a.is_target_identical(self.template_seq))

    def test_target_with_break(self):
        """Backbone gap breaks identity in target"""
        a = AlignmentMatcher(self.ali)
        with_break = Sequence("ACUGUGAY_UA[UACCU#PG")
        self.assertFalse(a.is_target_identical(with_break))
    
    def test_is_template_identical(self):
        a = AlignmentMatcher(self.ali)
        self.assertFalse(a.is_template_identical(self.target_seq))
        self.assertTrue(a.is_template_identical(self.template_seq))

    def test_template_with_break(self):
        """Backbone gap breaks identity in template"""
        a = AlignmentMatcher(self.ali)
        with_break = Sequence("GCGGAUUUALCUCAG")
        self.assertTrue(a.is_template_identical, with_break)
        
    def test_fix_template_seq(self):
        """Fix template sequence"""
        modified = Sequence("GCG7APU_UALCYC.G")
        expected  = 'GCG7A----PU_UALCUC.G'
        a = AlignmentMatcher(self.ali)
        a.fix_template_seq(modified)
        self.assertEqual(self.ali.template_seq, Sequence(expected.replace('-', '')))
        self.assertEqual(self.ali.aligned_template_seq, Sequence(expected))
        
    def test_adjust_target_seq(self):
        """Gaps inserted in target for extra _ in template."""
        modified = Sequence("GCG7APU_UALCYC.G")
        expected  = 'GCG7A----PU_UALCUC.G'
        a = AlignmentMatcher(self.ali)
        a.fix_template_seq(modified)
        self.assertEqual(self.ali.aligned_target_seq, Sequence("ACUGUGAYUA[-UACCU#PG"))
                                                                            
    def test_fix_example(self):
        """Real-world example from Irina"""
        ali = read_alignment(""">1EIY:C|PDBID|CHAIN|SEQUENCE
GCCGAGGUAGCUCAGUUGGUAGAGCAUGCGACUGAAAAUCGCAGUGUCCGCGGUUCGAUUCCGCGCCUCGGCACCA
>1EHZ:A|PDBID|CHAIN|SEQUENCE
GCGGAUUUAGCUCAGUUGGGAGAGCGCCAGACUGAAGAUCUGGAGGUCCUGUGUUCGAUCCACAGAAUUCGCACCA""")
        am = AlignmentMatcher(ali)
        seq = Sequence('GCGGAUUUALCUCAGDDGGGAGAGCRCCAGABU#AAYAP?UGGAG7UC?UGUGTPCG"UCCACAGAAUUCGCACCA')
        self.assertFalse(am.is_template_identical(seq))
        am.fix_template_seq(seq)
        self.assertTrue(am.is_template_identical(seq))

    def test_fix_alignment_with_gap(self):
        """Real-world exaple from nettab - 1qf6 modeling on 1c0a"""
        ali = read_alignment(""">1QF6
DDGGD-AGAGAAA
>1C0A
UCGGUUAGAA---""")
        true_target_seq = ali.aligned_sequences[0]
        am = AlignmentMatcher(ali)
        seq = Sequence('DCGGDDAGAA')
        self.assertFalse(am.is_template_identical(seq))
        am.fix_template_seq(seq)
        self.assertTrue(am.is_template_identical(seq))
        self.assertEqual(ali.aligned_sequences[0], true_target_seq)
    
if __name__ == '__main__':
    main()
    

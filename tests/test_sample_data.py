"""
Unit tests for sample data module
"""

import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sample_data import get_transcript, get_transcript_list, get_all_transcripts


class TestSampleData(unittest.TestCase):
    """Test cases for sample data functions"""
    
    def test_get_transcript_list(self):
        """Test getting list of available transcripts"""
        transcripts = get_transcript_list()
        
        self.assertIsInstance(transcripts, list)
        self.assertGreater(len(transcripts), 0)
        
        # Check structure of first transcript
        if transcripts:
            first = transcripts[0]
            self.assertIn('key', first)
            self.assertIn('company', first)
            self.assertIn('quarter', first)
            self.assertIn('date', first)
    
    def test_get_all_transcripts(self):
        """Test getting all transcript data"""
        all_transcripts = get_all_transcripts()
        
        self.assertIsInstance(all_transcripts, dict)
        self.assertGreater(len(all_transcripts), 0)
        
        # Check structure of first transcript
        for key, transcript in all_transcripts.items():
            self.assertIn('company', transcript)
            self.assertIn('quarter', transcript)
            self.assertIn('date', transcript)
            self.assertIn('transcript', transcript)
            self.assertIsInstance(transcript['transcript'], str)
            self.assertGreater(len(transcript['transcript']), 0)
            break  # Just check first one
    
    def test_get_transcript_with_valid_key(self):
        """Test getting a specific transcript with valid key"""
        # Get a valid key first
        transcripts = get_transcript_list()
        if transcripts:
            valid_key = transcripts[0]['key']
            transcript = get_transcript(valid_key)
            
            self.assertIsNotNone(transcript)
            self.assertIn('company', transcript)
            self.assertIn('quarter', transcript)
            self.assertIn('transcript', transcript)
    
    def test_get_transcript_with_invalid_key(self):
        """Test getting transcript with invalid key returns None"""
        transcript = get_transcript('invalid_key_12345')
        
        self.assertIsNone(transcript)
    
    def test_transcript_content_not_empty(self):
        """Test that transcript content is not empty"""
        all_transcripts = get_all_transcripts()
        
        for key, transcript in all_transcripts.items():
            self.assertGreater(len(transcript['transcript']), 100)
            self.assertIn('OPERATOR', transcript['transcript'].upper())
    
    def test_transcript_has_key_metrics(self):
        """Test that transcripts have key metrics"""
        all_transcripts = get_all_transcripts()
        
        for key, transcript in all_transcripts.items():
            if 'key_metrics' in transcript:
                self.assertIsInstance(transcript['key_metrics'], dict)


if __name__ == '__main__':
    unittest.main()

"""
Unit tests for the TranscriptAnalyzer class
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analyzer import TranscriptAnalyzer


class TestTranscriptAnalyzer(unittest.TestCase):
    """Test cases for TranscriptAnalyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test-api-key-12345"
        
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-api-key-12345'})
    @patch('analyzer.Anthropic')
    def test_analyzer_initialization(self, mock_anthropic):
        """Test that analyzer initializes correctly with API key"""
        analyzer = TranscriptAnalyzer()
        
        self.assertIsNotNone(analyzer)
        self.assertEqual(analyzer.api_key, 'test-api-key-12345')
        self.assertEqual(analyzer.model, 'claude-3-haiku-20240307')
        mock_anthropic.assert_called_once_with(api_key='test-api-key-12345')
    
    def test_analyzer_initialization_without_api_key(self):
        """Test that analyzer raises error without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                TranscriptAnalyzer()
            
            self.assertIn('ANTHROPIC_API_KEY', str(context.exception))
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-api-key-12345'})
    @patch('analyzer.Anthropic')
    def test_quick_scan_finds_hedging_language(self, mock_anthropic):
        """Test quick_scan detects hedging language"""
        analyzer = TranscriptAnalyzer()
        
        transcript = """
        We believe that our product will be successful. 
        We expect to see growth in Q2. 
        Hopefully, we can maintain our market position.
        """
        
        result = analyzer.quick_scan(transcript)
        
        self.assertIn('total_hedging_phrases', result)
        self.assertIn('examples', result)
        self.assertGreater(result['total_hedging_phrases'], 0)
        self.assertIsInstance(result['examples'], list)
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-api-key-12345'})
    @patch('analyzer.Anthropic')
    def test_quick_scan_with_clean_transcript(self, mock_anthropic):
        """Test quick_scan with transcript containing no hedging language"""
        analyzer = TranscriptAnalyzer()
        
        transcript = "Revenue increased by 20%. Profit margins improved significantly."
        
        result = analyzer.quick_scan(transcript)
        
        self.assertEqual(result['total_hedging_phrases'], 0)
        self.assertEqual(len(result['examples']), 0)
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-api-key-12345'})
    @patch('analyzer.Anthropic')
    def test_generate_summary_stats(self, mock_anthropic):
        """Test summary stats generation"""
        analyzer = TranscriptAnalyzer()
        
        analysis_result = {
            'confidence_score': 75,
            'risk_level': 'MEDIUM',
            'hedging_language': [{'phrase': 'we believe'}, {'phrase': 'hopefully'}],
            'key_concerns': [{'concern': 'Market uncertainty'}],
            'question_dodging': [{'question': 'Q1', 'answer': 'A1'}],
            'positive_signals': ['Strong revenue']
        }
        
        stats = analyzer.generate_summary_stats(analysis_result)
        
        self.assertEqual(stats['confidence_score'], 75)
        self.assertEqual(stats['risk_level'], 'MEDIUM')
        self.assertEqual(stats['hedging_count'], 2)
        self.assertEqual(stats['concerns_count'], 1)
        self.assertEqual(stats['dodged_questions'], 1)
        self.assertEqual(stats['positive_signals'], 1)
        self.assertIn('health_score', stats)
        self.assertIsInstance(stats['health_score'], int)
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-api-key-12345'})
    @patch('analyzer.Anthropic')
    def test_highlight_transcript(self, mock_anthropic):
        """Test transcript highlighting"""
        analyzer = TranscriptAnalyzer()
        
        transcript = "We believe this is a good strategy."
        concerns = {
            'hedging_language': [
                {'phrase': 'we believe', 'context': 'We believe this is good'}
            ]
        }
        
        highlighted = analyzer.highlight_transcript(transcript, concerns)
        
        self.assertIn('highlight-hedge', highlighted)
        self.assertIn('we believe', highlighted.lower())
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-api-key-12345'})
    @patch('analyzer.Anthropic')
    def test_analyze_transcript_with_valid_json_response(self, mock_anthropic):
        """Test analyze_transcript with valid JSON response from Claude"""
        # Create mock response
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = json.dumps({
            'confidence_score': 80,
            'overall_assessment': 'Good transparency',
            'hedging_language': [],
            'key_concerns': [],
            'question_dodging': [],
            'positive_signals': ['Clear communication'],
            'risk_level': 'LOW'
        })
        mock_response.usage = MagicMock()
        
        mock_client.messages.create.return_value = mock_response
        
        analyzer = TranscriptAnalyzer()
        result = analyzer.analyze_transcript(
            'Test transcript',
            'TestCorp',
            'Q1 2024'
        )
        
        self.assertEqual(result['confidence_score'], 80)
        self.assertEqual(result['risk_level'], 'LOW')
        self.assertIn('_raw_response', result)
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-api-key-12345'})
    @patch('analyzer.Anthropic')
    def test_analyze_transcript_with_invalid_json_response(self, mock_anthropic):
        """Test analyze_transcript handles invalid JSON gracefully"""
        # Create mock response with invalid JSON
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = '{"invalid": json here}'
        mock_response.usage = MagicMock()
        
        mock_client.messages.create.return_value = mock_response
        
        analyzer = TranscriptAnalyzer()
        result = analyzer.analyze_transcript(
            'Test transcript',
            'TestCorp',
            'Q1 2024'
        )
        
        # Should return fallback structure
        self.assertIn('confidence_score', result)
        self.assertIn('hedging_language', result)
        self.assertIn('_raw_response', result)


if __name__ == '__main__':
    unittest.main()

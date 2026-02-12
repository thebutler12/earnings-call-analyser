"""
Unit tests for the Flask application
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app as flask_app


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        flask_app.app.config['TESTING'] = True
        self.client = flask_app.app.test_client()
    
    def test_index_route(self):
        """Test that index route returns HTML"""
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Earnings Call Analyser', response.data)
    
    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn('success', data)
        self.assertIn('status', data)
        self.assertTrue(data['success'])
    
    def test_transcripts_list_endpoint(self):
        """Test transcripts list endpoint"""
        response = self.client.get('/api/transcripts')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn('success', data)
        self.assertIn('transcripts', data)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['transcripts'], list)
    
    def test_get_transcript_detail(self):
        """Test getting a specific transcript"""
        # First get the list to find a valid key
        list_response = self.client.get('/api/transcripts')
        transcripts = json.loads(list_response.data)['transcripts']
        
        if transcripts:
            key = transcripts[0]['key']
            response = self.client.get(f'/api/transcript/{key}')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            
            self.assertTrue(data['success'])
            self.assertIn('transcript', data)
    
    def test_get_nonexistent_transcript(self):
        """Test getting a transcript that doesn't exist"""
        response = self.client.get('/api/transcript/nonexistent_key')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    @patch('app.analyzer')
    def test_analyze_endpoint_without_transcript(self, mock_analyzer):
        """Test analyze endpoint without providing transcript"""
        response = self.client.post(
            '/api/analyze',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    @patch('app.analyzer')
    def test_analyze_endpoint_with_valid_data(self, mock_analyzer):
        """Test analyze endpoint with valid transcript data"""
        # Mock the analyzer methods
        mock_analyzer.analyze_transcript.return_value = {
            'confidence_score': 75,
            'overall_assessment': 'Test assessment',
            'hedging_language': [],
            'key_concerns': [],
            'question_dodging': [],
            'positive_signals': [],
            'risk_level': 'MEDIUM',
            '_raw_response': 'raw response text'
        }
        
        mock_analyzer.generate_summary_stats.return_value = {
            'confidence_score': 75,
            'risk_level': 'MEDIUM',
            'hedging_count': 0,
            'concerns_count': 0,
            'dodged_questions': 0,
            'positive_signals': 0,
            'health_score': 75
        }
        
        mock_analyzer.highlight_transcript.return_value = 'highlighted text'
        
        response = self.client.post(
            '/api/analyze',
            data=json.dumps({
                'transcript_text': 'Test transcript',
                'company_name': 'TestCorp',
                'quarter': 'Q1 2024'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertIn('analysis', data)
        self.assertIn('stats', data)
        self.assertIn('highlighted_transcript', data)
        self.assertIn('raw_anthropic_response', data)
    
    @patch('app.analyzer')
    def test_quick_scan_endpoint(self, mock_analyzer):
        """Test quick scan endpoint"""
        mock_analyzer.quick_scan.return_value = {
            'total_hedging_phrases': 3,
            'examples': [
                {'phrase': 'we believe', 'context': 'test context'}
            ]
        }
        
        response = self.client.post(
            '/api/quick-scan',
            data=json.dumps({
                'transcript_text': 'We believe this will work'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertIn('scan_result', data)
    
    def test_404_error_handler(self):
        """Test 404 error handler"""
        response = self.client.get('/nonexistent-route')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        
        self.assertFalse(data['success'])
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()

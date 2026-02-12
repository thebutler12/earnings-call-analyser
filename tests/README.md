# Tests

This directory contains unit tests for the Earnings Call Analyser application.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── test_analyzer.py         # Tests for TranscriptAnalyzer class
├── test_app.py             # Tests for Flask application endpoints
├── test_sample_data.py     # Tests for sample data functions
├── run_tests.py            # Test runner script
├── requirements-test.txt   # Testing dependencies
└── README.md              # This file
```

## Running Tests

### Using unittest (built-in)

Run all tests:
```bash
python -m unittest discover tests
```

Run specific test file:
```bash
python -m unittest tests.test_analyzer
```

Run specific test class:
```bash
python -m unittest tests.test_analyzer.TestTranscriptAnalyzer
```

Run specific test method:
```bash
python -m unittest tests.test_analyzer.TestTranscriptAnalyzer.test_analyzer_initialization
```

### Using the test runner

```bash
python tests/run_tests.py
```

### Using pytest (optional)

Install pytest first:
```bash
pip install -r tests/requirements-test.txt
```

Run all tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html tests/
```

Run with verbose output:
```bash
pytest -v tests/
```

## Test Coverage

### Current Test Coverage

- **test_analyzer.py**: Tests for the core analysis engine
  - Initialization with/without API key
  - Quick scan functionality
  - Summary statistics generation
  - Transcript highlighting
  - Full analysis with mocked API responses
  - Error handling for invalid JSON

- **test_app.py**: Tests for Flask application
  - Route handlers (index, health, transcripts)
  - API endpoints (analyze, quick-scan)
  - Error handling (404, 400, 500)
  - Request/response validation

- **test_sample_data.py**: Tests for sample data
  - Transcript list retrieval
  - Individual transcript retrieval
  - Data structure validation
  - Content validation

## Writing New Tests

### Test Naming Convention

- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<what_is_being_tested>`

### Example Test

```python
import unittest
from unittest.mock import patch

class TestMyFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.test_data = "example"
    
    def test_feature_works(self):
        """Test that feature works as expected"""
        result = my_function(self.test_data)
        self.assertEqual(result, "expected")
    
    @patch('module.external_dependency')
    def test_with_mock(self, mock_dep):
        """Test with mocked dependency"""
        mock_dep.return_value = "mocked"
        result = my_function()
        self.assertEqual(result, "mocked")
```

## Mocking External Dependencies

Tests use `unittest.mock` to mock external dependencies:

- **Anthropic API**: Mocked to avoid real API calls
- **Environment variables**: Patched for testing different configurations
- **File system**: Can be mocked if needed

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    python -m unittest discover tests
```

## Test Best Practices

1. **Isolation**: Each test should be independent
2. **Mocking**: Mock external dependencies (APIs, databases)
3. **Coverage**: Aim for >80% code coverage
4. **Speed**: Tests should run quickly (<5 seconds total)
5. **Clarity**: Test names should describe what they test
6. **Assertions**: Use specific assertions (assertEqual, assertIn, etc.)

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running tests from the project root:
```bash
cd /path/to/earnings-call-analyser
python -m unittest discover tests
```

### API Key Errors

Tests mock the Anthropic API, so you don't need a real API key. If you see API key errors, check that the mocking is set up correctly.

### Module Not Found

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

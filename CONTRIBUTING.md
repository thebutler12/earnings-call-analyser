# Contributing to Earnings Call Nonsense Detector

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Run setup: `./setup.sh`
4. Create a feature branch: `git checkout -b feature/your-feature`

## Project Structure

```
earnings-nonsense-detector/
├── app.py                  # Flask application
├── analyzer.py            # LLM analysis logic
├── sample_data.py         # Sample transcripts
├── static/
│   ├── styles.css        # UI styling
│   └── script.js         # Frontend logic
└── templates/
    └── index.html        # Main template
```

## Adding New Features

### Adding New Analysis Types

To add a new type of analysis (e.g., tone analysis):

1. Add method to `analyzer.py`:
```python
def analyze_tone(self, transcript_text):
    # Your analysis logic
    pass
```

2. Update the analysis prompt in `analyze_transcript()`
3. Add UI elements in `index.html`
4. Add display logic in `script.js`

### Adding New Data Sources

To integrate a new data source (e.g., SEC EDGAR):

1. Create new module: `data_sources/sec_edgar.py`
2. Implement fetch methods
3. Update `sample_data.py` to use new source
4. Add UI for source selection

### Adding Tests

We welcome test contributions! Create tests in a `tests/` directory:

```python
# tests/test_analyzer.py
import unittest
from analyzer import TranscriptAnalyzer

class TestAnalyzer(unittest.TestCase):
    def test_quick_scan(self):
        analyzer = TranscriptAnalyzer()
        result = analyzer.quick_scan("We believe this is good")
        self.assertGreater(result['total_hedging_phrases'], 0)
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update README.md if you've added user-facing features
5. Submit PR with clear description of changes

## Questions?

Open an issue for discussion before starting major work.

Happy coding! 🎯

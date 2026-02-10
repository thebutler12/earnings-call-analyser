# Earnings Call Nonsense Detector 🎯

A proof-of-concept application that uses LLMs to analyze earnings call transcripts and identify potential red flags, hedging language, and inconsistencies that might indicate management uncertainty or misdirection.

## What It Does

This application analyzes earnings call transcripts to help investors cut through corporate speak and identify potential concerns:

- **Hedging Language Detection**: Flags vague phrases like "we believe," "we expect," "hopefully," etc.
- **Confidence Scoring**: Analyzes overall tone and certainty levels in executive statements
- **Key Concerns Extraction**: Uses LLM to identify the most significant concerns or risks mentioned
- **Question Dodging**: Highlights when executives give non-answers to analyst questions
- **Visual Timeline**: Shows sentiment and confidence trends across different sections of the call

## Why I Built This

Earnings calls are critical for investment decisions, but they're often filled with carefully crafted language designed to manage perceptions. This tool helps investors:
- Save time by highlighting the most important red flags
- Spot patterns of evasive language
- Get an AI-powered "second opinion" on management credibility
- Compare language patterns across quarters (future enhancement)

This is particularly relevant in financial services for:
- Equity research teams doing due diligence
- Risk assessment of portfolio companies
- Automated screening of multiple companies at scale

## Architecture & Design Decisions

### Technology Stack
- **Backend**: Python with Flask (lightweight, perfect for POC)
- **LLM**: Anthropic Claude API (excellent at nuanced text analysis)
- **Frontend**: Vanilla HTML/CSS/JavaScript (no build step needed for Codespaces)
- **Data Source**: Sample transcript data (in production: SEC EDGAR, earnings call providers)

### Key Design Decisions

1. **Why Claude over GPT?**
   - Superior at nuanced analysis of hedging language
   - Better at following complex analytical instructions
   - 200K context window allows analyzing entire transcripts

2. **Streaming Analysis**
   - Backend streams results to frontend as they're generated
   - Better UX for longer transcripts
   - Shows progress during LLM processing

3. **Modular Prompt Design**
   - Separate prompts for different analysis types (hedging, sentiment, concerns)
   - Easier to refine and test individual components
   - Can be parallelized in future versions

4. **Simple Data Model**
   - For POC, uses in-memory sample data
   - Production would use database with historical transcript storage
   - Designed for easy extension to multi-quarter comparisons

5. **No Frontend Framework**
   - Reduces complexity for Codespaces deployment
   - No build step or npm dependencies for frontend
   - Faster iteration during development

### Trade-offs

- **Sample Data vs Real-time Fetching**: Using embedded sample transcripts keeps the POC focused on the analysis, but limits scope. Next iteration would integrate SEC EDGAR API.
- **Single LLM Pass vs Multi-Agent**: Currently uses a single LLM call for efficiency. A multi-agent approach (bull vs bear analysts) would be more engaging but slower.
- **In-memory vs Database**: No persistence keeps deployment simple but means no historical tracking yet.

## How to Run Locally

### Prerequisites
- Python 3.9+
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Setup Instructions

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd earnings-bs-detector
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

5. **Run the application**
```bash
python app.py
```

6. **Open in browser**
Navigate to `http://localhost:5000`

### Running in GitHub Codespaces

1. Open the repository in Codespaces
2. The environment will automatically install dependencies
3. Create a `.env` file with your `ANTHROPIC_API_KEY`
4. Run `python app.py`
5. Click "Open in Browser" when the port forwarding notification appears

## How to Use

1. Select a sample earnings call from the dropdown (or paste your own transcript)
2. Click "Analyze Transcript"
3. Watch as the analysis streams in:
   - Overall confidence score
   - Hedging language instances
   - Key concerns identified
   - Question dodging examples
4. Review the highlighted sections in the original transcript

## Next Steps & Future Enhancements

If I were to continue building this out, here's what I'd add next:

### Short-term (1-2 weeks)
- **Historical Comparison**: Compare current call to previous quarters to spot changes in tone
- **Company Database**: Store analyzed transcripts for trend analysis
- **Export Reports**: Generate PDF reports of analysis for sharing
- **More Data Sources**: Integrate SEC EDGAR API for automatic transcript fetching
- **Batch Processing**: Analyze multiple companies simultaneously

### Medium-term (1-2 months)
- **Multi-Agent Debate**: Create "bull" and "bear" analyst agents that debate the transcript
- **Quantitative Correlation**: Link hedging language to actual stock performance post-call
- **Industry Benchmarking**: Compare company's language patterns to industry peers
- **Custom Dictionaries**: Allow users to define their own red flag terms
- **API Endpoint**: RESTful API for integration with other tools

### Long-term (3-6 months)
- **Real-time Processing**: Analyze calls as they happen (via live transcription)
- **ML Fine-tuning**: Train models on labeled "misleading" vs "transparent" statements
- **Voice Analysis**: Incorporate tone/stress detection from audio
- **Knowledge Graph**: Build relationship maps between statements and outcomes
- **Portfolio Integration**: Auto-analyze all calls for companies in a user's portfolio

### Technical Improvements
- **Caching Layer**: Redis for caching analysis results
- **Async Processing**: Celery for background job processing
- **Testing Suite**: Comprehensive unit and integration tests
- **Production Deployment**: Docker containerization, CI/CD pipeline
- **Authentication**: User accounts and API key management
- **Rate Limiting**: Protect against API abuse

## Project Structure

```
earnings-bs-detector/
├── app.py                 # Flask application and API endpoints
├── analyzer.py           # Core LLM analysis logic
├── sample_data.py        # Sample earnings call transcripts
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variable template
├── README.md            # This file
├── static/
│   ├── styles.css       # UI styling
│   └── script.js        # Frontend logic
└── templates/
    └── index.html       # Main UI template
```

## Technologies Used

- **Python 3.9+**: Core backend language
- **Flask**: Web framework for API and serving frontend
- **Anthropic Claude**: LLM for transcript analysis
- **HTML/CSS/JavaScript**: Frontend interface
- **python-dotenv**: Environment variable management

## License

MIT License - feel free to use this for your own projects!

## Acknowledgments

Built as a technical exercise for an Innovation Engineer role. Thanks to the team for the creative freedom to explore this idea!

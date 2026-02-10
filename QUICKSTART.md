# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## For GitHub Codespaces (Easiest)

1. **Upload to GitHub**
   - Create new repository on GitHub
   - Upload this folder or push via git

2. **Open Codespaces**
   - Click "Code" → "Codespaces" → "Create codespace"
   - Wait for environment to build (~1 minute)

3. **Configure API Key**
   ```bash
   cp .env.example .env
   nano .env  # Add your ANTHROPIC_API_KEY
   ```

4. **Run**
   ```bash
   python app.py
   ```
   - Click "Open in Browser" when port forwarding notification appears
   - Done! 🎉

## For Local Development

1. **Setup**
   ```bash
   ./setup.sh
   source venv/bin/activate
   ```

2. **Configure**
   - Edit `.env` file
   - Add your `ANTHROPIC_API_KEY`

3. **Run**
   ```bash
   python app.py
   ```
   - Open http://localhost:5000

## Get API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to "API Keys"
4. Create new key
5. Copy and paste into `.env` file

## Test It Works

```bash
python test_setup.py
```

This checks everything is configured correctly.

## First Analysis

1. Open the app in browser
2. Select a sample transcript (e.g., "TechCorp Inc.")
3. Click "Analyze Transcript"
4. Wait ~10-20 seconds
5. Review the results!

## Troubleshooting

**"Analyzer not initialized"**
- Check your API key is set in `.env`
- Make sure `.env` file exists

**Port 5000 in use**
```bash
lsof -ti:5000 | xargs kill -9
python app.py
```

**Dependencies missing**
```bash
pip install -r requirements.txt
```

## What to Demo

1. **Show the UI** - Clean, professional interface
2. **Run Analysis** - Pick "RetailCo" (has most red flags)
3. **Explain Results**:
   - Confidence score (lower is more concerning)
   - Hedging language detection
   - Question dodging analysis
   - Key concerns identified
4. **Show Technical**:
   - Clean code structure
   - LLM integration
   - Streaming results
   - Highlighted transcript

## Next Steps for Interview

If asked "What would you build next?", refer to the "Next Steps" section in README.md:
- Historical comparison
- Multi-agent debates
- Real-time processing
- API endpoints
- Database integration

Good luck! 🎯

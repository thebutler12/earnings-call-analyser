# Deployment Guide

This guide covers deploying the Earnings Call Nonsense Detector to various platforms.

## GitHub Codespaces (Recommended for Demo)

GitHub Codespaces provides a cloud-based development environment that's perfect for demos and testing.

### Setup

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Open in Codespaces**
   - Go to your repository on GitHub
   - Click the green "Code" button
   - Select "Codespaces" tab
   - Click "Create codespace on main"

3. **Configure Environment**
   - Once Codespace opens, create `.env` file:
     ```bash
     cp .env.example .env
     nano .env  # or use VS Code editor
     ```
   - Add your `ANTHROPIC_API_KEY`

4. **Run the Application**
   ```bash
   python app.py
   ```
   - Codespaces will automatically forward port 5000
   - Click "Open in Browser" when prompted

### Features
- ✅ Automatic dependency installation
- ✅ Pre-configured Python environment
- ✅ Port forwarding
- ✅ VS Code in browser
- ✅ Free tier available

## Local Development

### Prerequisites
- Python 3.9+
- pip
- Git

### Setup
```bash
# Clone repository
git clone <repo-url>
cd earnings-nonsense-detector

# Run setup script
chmod +x setup.sh
./setup.sh

# Activate environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Configure .env
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run application
python app.py

# Open browser
# Navigate to http://localhost:5000
```

## Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t earnings-nonsense-detector .
docker run -p 5000:5000 --env-file .env earnings-nonsense-detector
```

## Cloud Platforms

### Heroku

1. Create `Procfile`:
   ```
   web: python app.py
   ```

2. Deploy:
   ```bash
   heroku create earnings-nonsense-detector
   heroku config:set ANTHROPIC_API_KEY=your_key_here
   git push heroku main
   ```

### Google Cloud Run

1. Add to `requirements.txt`:
   ```
   gunicorn==21.2.0
   ```

2. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

3. Deploy:
   ```bash
   gcloud run deploy earnings-nonsense-detector \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### AWS Elastic Beanstalk

1. Create `.ebextensions/python.config`:
   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: app:app
   ```

2. Deploy:
   ```bash
   eb init -p python-3.11 earnings-nonsense-detector
   eb create earnings-nonsense-detector-env
   eb setenv ANTHROPIC_API_KEY=your_key_here
   eb deploy
   ```

## Environment Variables

Required:
- `ANTHROPIC_API_KEY`: Your Anthropic API key

Optional:
- `FLASK_ENV`: Set to `production` for deployment
- `PORT`: Port to run on (default: 5000)
- `FLASK_DEBUG`: Set to `0` for production

## Production Considerations

### Security
- Never commit `.env` file
- Use environment variable management (GitHub Secrets, AWS Secrets Manager, etc.)
- Enable HTTPS
- Add rate limiting
- Implement authentication if needed

### Performance
- Use production WSGI server (gunicorn, uwsgi)
- Enable caching for analysis results
- Consider async processing for long-running analyses
- Add database for storing results

### Monitoring
- Add logging (Python logging module)
- Implement error tracking (Sentry)
- Monitor API usage and costs
- Set up uptime monitoring

### Example Production Config

```python
# app.py (production additions)
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

# Apply to analyze endpoint
@app.route('/api/analyze', methods=['POST'])
@limiter.limit("10 per minute")
def analyze_transcript():
    # ... existing code
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### API Key Issues
- Verify key is set: `echo $ANTHROPIC_API_KEY`
- Check .env file exists and is loaded
- Ensure key has correct permissions in Anthropic console

### Codespaces Specific
- If port forwarding doesn't work, manually forward port 5000
- Clear browser cache if UI doesn't update
- Restart Codespace if environment issues persist

## Testing Deployment

Use the test script to verify everything works:

```bash
python test_setup.py
```

This will check:
- ✅ All required files present
- ✅ Dependencies installed
- ✅ Environment variables set
- ✅ Sample data loads
- ✅ Analyzer initializes

## Support

For issues:
1. Check the troubleshooting section
2. Review logs for error messages
3. Verify API key is valid
4. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Environment details

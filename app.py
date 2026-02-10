"""
Flask application for Earnings Call Nonsense Detector.
Provides web UI and API endpoints for transcript analysis.
"""

from flask import Flask, render_template, request, jsonify, Response
import json
import os
import logging
from dotenv import load_dotenv

from analyzer import TranscriptAnalyzer
from sample_data import get_transcript, get_transcript_list, get_all_transcripts

# Load environment variables
load_dotenv()

# Set up logging for Flask app
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize analyzer
try:
    analyzer = TranscriptAnalyzer()
    logger.info("✅ TranscriptAnalyzer initialized successfully")
except ValueError as e:
    logger.error(f"❌ Failed to initialize analyzer: {e}")
    print(f"Warning: {e}")
    print("Please set ANTHROPIC_API_KEY in .env file")
    analyzer = None

@app.route('/')
def index():
    """Serve the main UI"""
    return render_template('index.html')

@app.route('/api/transcripts', methods=['GET'])
def list_transcripts():
    """Get list of available sample transcripts"""
    transcripts = get_transcript_list()
    return jsonify({
        "success": True,
        "transcripts": transcripts
    })

@app.route('/api/transcript/<key>', methods=['GET'])
def get_transcript_detail(key):
    """Get full details of a specific transcript"""
    transcript = get_transcript(key)
    
    if not transcript:
        return jsonify({
            "success": False,
            "error": "Transcript not found"
        }), 404
    
    return jsonify({
        "success": True,
        "transcript": transcript
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_transcript():
    """
    Analyze a transcript for red flags and concerns.
    Expects JSON with: transcript_text, company_name, quarter
    """
    logger.info("📊 Received analysis request")
    
    if not analyzer:
        logger.error("❌ Analyzer not initialized")
        return jsonify({
            "success": False,
            "error": "Analyzer not initialized. Please check ANTHROPIC_API_KEY"
        }), 500
    
    data = request.get_json()
    
    transcript_text = data.get('transcript_text')
    company_name = data.get('company_name', 'Unknown Company')
    quarter = data.get('quarter', 'Unknown Quarter')
    
    logger.info(f"📋 Analysis request details:")
    logger.info(f"   Company: {company_name}")
    logger.info(f"   Quarter: {quarter}")
    logger.info(f"   Transcript length: {len(transcript_text) if transcript_text else 0} characters")
    
    if not transcript_text:
        logger.warning("❌ No transcript text provided")
        return jsonify({
            "success": False,
            "error": "No transcript text provided"
        }), 400
    
    # Perform analysis
    try:
        logger.info("🤖 Starting Anthropic API analysis...")
        analysis_result = analyzer.analyze_transcript(
            transcript_text=transcript_text,
            company_name=company_name,
            quarter=quarter
        )
        
        logger.info("📈 Generating summary stats...")
        # Generate summary stats
        stats = analyzer.generate_summary_stats(analysis_result)
        
        logger.info("🎨 Generating highlighted transcript...")
        # Generate highlighted transcript
        highlighted_text = analyzer.highlight_transcript(
            transcript_text=transcript_text,
            concerns=analysis_result
        )
        
        logger.info("✅ Analysis completed successfully")
        logger.info(f"   Confidence Score: {analysis_result.get('confidence_score', 'N/A')}")
        logger.info(f"   Risk Level: {analysis_result.get('risk_level', 'N/A')}")
        logger.info(f"   Hedging Language Found: {len(analysis_result.get('hedging_language', []))}")
        logger.info(f"   Key Concerns: {len(analysis_result.get('key_concerns', []))}")
        
        # Extract raw response for sidebar
        raw_response = analysis_result.pop('_raw_response', None)
        
        return jsonify({
            "success": True,
            "analysis": analysis_result,
            "stats": stats,
            "highlighted_transcript": highlighted_text,
            "raw_anthropic_response": raw_response
        })
        
    except Exception as e:
        logger.error(f"❌ Analysis error: {str(e)}")
        logger.error(f"   Exception type: {type(e).__name__}")
        return jsonify({
            "success": False,
            "error": f"Analysis error: {str(e)}"
        }), 500

@app.route('/api/quick-scan', methods=['POST'])
def quick_scan():
    """
    Quick scan for hedging language without full LLM analysis.
    Faster but less sophisticated than full analysis.
    """
    if not analyzer:
        return jsonify({
            "success": False,
            "error": "Analyzer not initialized"
        }), 500
    
    data = request.get_json()
    transcript_text = data.get('transcript_text')
    
    if not transcript_text:
        return jsonify({
            "success": False,
            "error": "No transcript text provided"
        }), 400
    
    try:
        result = analyzer.quick_scan(transcript_text)
        return jsonify({
            "success": True,
            "scan_result": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Scan error: {str(e)}"
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "status": "healthy",
        "analyzer_ready": analyzer is not None,
        "sample_transcripts": len(get_all_transcripts())
    })

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║  Earnings Call Nonsense Detector                          ║
    ║  Starting on http://localhost:{port}                         ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    if not analyzer:
        print("⚠️  Warning: ANTHROPIC_API_KEY not set. Analysis will not work.")
        print("   Please create a .env file with your API key.")
    else:
        print("✅ Analyzer ready")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

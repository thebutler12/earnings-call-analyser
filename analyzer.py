"""
Core analysis module for earnings call transcripts.
Uses Anthropic's Claude to detect hedging language, sentiment, and red flags.
"""

import os
import re
import logging
from anthropic import Anthropic

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranscriptAnalyzer:
    def __init__(self, api_key=None):
        """Initialize the analyzer with Anthropic API key"""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-haiku-20240307"
        
        logger.info(f"TranscriptAnalyzer initialized with model: {self.model}")
        logger.info(f"API key configured: {bool(self.api_key)}")
    
    def analyze_transcript(self, transcript_text, company_name, quarter):
        """
        Analyze earnings call transcript for red flags and concerns.
        Returns structured analysis results.
        """
        
        # Build comprehensive analysis prompt
        analysis_prompt = f"""You are an expert financial analyst reviewing an earnings call transcript for {company_name} ({quarter}). 

Analyze this transcript and identify potential red flags, hedging language, and areas of concern.

CRITICAL: Return ONLY valid JSON. Do NOT use quotation marks or apostrophes inside your text values. Rephrase to avoid them.

Example of GOOD formatting:
"reason": "The phrase indicates uncertainty about future performance"

Example of BAD formatting (DO NOT DO THIS):
"reason": "The phrase "we believe" indicates uncertainty"

Return your analysis in this exact JSON format:

{{
  "confidence_score": 75,
  "overall_assessment": "Brief summary here without any quotes",
  "hedging_language": [
    {{
      "phrase": "we believe",
      "context": "Surrounding text without quotes",
      "severity": "medium",
      "reason": "Explanation without quotes"
    }}
  ],
  "key_concerns": [
    {{
      "concern": "Title here",
      "description": "Details without quotes",
      "evidence": "Paraphrased evidence without quotes",
      "impact": "Impact description"
    }}
  ],
  "question_dodging": [
    {{
      "question": "The analyst question",
      "answer": "Management response",
      "analysis": "Your analysis without quotes"
    }}
  ],
  "positive_signals": [
    "Positive point one",
    "Positive point two"
  ],
  "risk_level": "MEDIUM"
}}

TRANSCRIPT:
{transcript_text}

Remember: NO quotes or apostrophes inside your text values. Rephrase everything."""

        try:
            logger.info(f"Starting analysis for {company_name} ({quarter})")
            logger.info(f"Transcript length: {len(transcript_text)} characters")
            logger.info(f"Using model: {self.model}")
            
            # Call Claude API
            logger.info("Sending request to Anthropic API...")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,  # Lower temperature for more consistent analysis
                messages=[{
                    "role": "user",
                    "content": analysis_prompt
                }]
            )
            
            logger.info("✅ Received response from Anthropic API")
            logger.info(f"Response usage: {getattr(response, 'usage', 'N/A')}")
            
            # Extract the response text
            result_text = response.content[0].text
            logger.info(f"Raw response length: {len(result_text)} characters")
            logger.info("Raw Anthropic response:")
            logger.info("=" * 50)
            logger.info(result_text)
            logger.info("=" * 50)
            
            # Try to extract JSON from response (Claude sometimes includes explanation)
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                import json
                logger.info("✅ Found JSON in response, parsing...")
                
                json_text = json_match.group()
                
                try:
                    result = json.loads(json_text)
                    logger.info(f"✅ Successfully parsed JSON with keys: {list(result.keys())}")
                    # Add raw response to result
                    result['_raw_response'] = result_text
                except json.JSONDecodeError as e:
                    logger.error(f"❌ JSON parsing failed: {str(e)}")
                    logger.error(f"❌ Error at position {e.pos}: {json_text[max(0, e.pos-50):e.pos+50]}")
                    
                    # Simpler approach: Use a more lenient parser
                    try:
                        # Try to fix by replacing quotes in a smarter way
                        # Look for patterns like: "text": "value with "quotes" inside"
                        # and replace inner quotes with single quotes
                        
                        # Pattern to match JSON string values
                        # This finds "key": "value" pairs
                        def fix_value(match):
                            key = match.group(1)
                            value = match.group(2)
                            # Replace quotes inside the value with single quotes
                            fixed_value = value.replace('"', "'")
                            return f'"{key}": "{fixed_value}"'
                        
                        # Match "key": "value" where value might contain quotes
                        # This pattern is more careful about what it matches
                        pattern = r'"([^"]+)":\s*"([^"]*(?:"[^"]*)*)"'
                        
                        # Try multiple passes to fix nested issues
                        fixed_json = json_text
                        for _ in range(3):  # Try up to 3 passes
                            try:
                                # Test if it parses
                                json.loads(fixed_json)
                                break
                            except:
                                # Try to fix more
                                # Simple approach: find ": " followed by quoted text and fix internal quotes
                                lines = fixed_json.split('\n')
                                fixed_lines = []
                                for line in lines:
                                    if '": "' in line and line.count('"') > 4:
                                        # This line likely has quotes inside a value
                                        # Find the value part after ": "
                                        parts = line.split('": "', 1)
                                        if len(parts) == 2:
                                            key_part = parts[0] + '": "'
                                            value_part = parts[1]
                                            # Find the closing quote (last quote before comma or end)
                                            if value_part.endswith('",') or value_part.endswith('"'):
                                                # Replace internal quotes with single quotes
                                                if value_part.endswith('",'):
                                                    value_content = value_part[:-2]
                                                    value_content = value_content.replace('"', "'")
                                                    line = key_part + value_content + '",'
                                                else:
                                                    value_content = value_part[:-1]
                                                    value_content = value_content.replace('"', "'")
                                                    line = key_part + value_content + '"'
                                    fixed_lines.append(line)
                                fixed_json = '\n'.join(fixed_lines)
                        
                        result = json.loads(fixed_json)
                        logger.info("✅ Successfully parsed JSON after fixing quotes")
                        result['_raw_response'] = result_text
                    except Exception as fix_error:
                        logger.warning(f"❌ Could not fix JSON: {fix_error}")
                        # Last resort: return a simplified result with the raw response
                        result = {
                            "error": "Could not parse analysis - JSON syntax error",
                            "raw_response": result_text,
                            "confidence_score": 50,
                            "overall_assessment": "Analysis completed but JSON parsing failed. Check raw response for details.",
                            "hedging_language": [],
                            "key_concerns": [],
                            "question_dodging": [],
                            "positive_signals": [],
                            "risk_level": "UNKNOWN",
                            "_raw_response": result_text
                        }
            else:
                # Fallback if no JSON found
                logger.warning("❌ No JSON found in response, returning raw response")
                result = {
                    "error": "Could not parse analysis",
                    "raw_response": result_text,
                    "_raw_response": result_text
                }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            return {
                "error": f"Analysis failed: {str(e)}",
                "confidence_score": 0
            }
    
    def quick_scan(self, transcript_text):
        """
        Faster scan for basic hedging language without full LLM analysis.
        Useful for initial screening.
        """
        hedging_patterns = [
            r'\b(we believe|we think|hopefully|we expect|we anticipate)\b',
            r'\b(difficult to predict|uncertain|challenging|it\'s hard to)\b',
            r'\b(may|might|could|should|would)\b',
            r'\b(early days|early signs|promising signs)\b',
            r'\b(we\'re optimistic|we\'re encouraged|we feel good)\b'
        ]
        
        findings = []
        for pattern in hedging_patterns:
            matches = re.finditer(pattern, transcript_text, re.IGNORECASE)
            for match in matches:
                # Get context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(transcript_text), match.end() + 50)
                context = transcript_text[start:end]
                
                findings.append({
                    "phrase": match.group(),
                    "context": context.strip()
                })
        
        return {
            "total_hedging_phrases": len(findings),
            "examples": findings[:10]  # Return first 10 examples
        }
    
    def highlight_transcript(self, transcript_text, concerns):
        """
        Generate HTML-highlighted version of transcript based on analysis.
        """
        highlighted = transcript_text
        
        # Highlight hedging language in yellow
        if "hedging_language" in concerns:
            for item in concerns["hedging_language"]:
                phrase = item.get("phrase", "")
                if phrase:
                    # Escape special regex characters
                    escaped_phrase = re.escape(phrase)
                    pattern = re.compile(f'({escaped_phrase})', re.IGNORECASE)
                    highlighted = pattern.sub(
                        r'<span class="highlight-hedge" title="Hedging language">\1</span>',
                        highlighted
                    )
        
        # Highlight question dodging in orange
        if "question_dodging" in concerns:
            for item in concerns["question_dodging"]:
                answer = item.get("answer", "")[:100]  # First 100 chars
                if answer:
                    escaped_answer = re.escape(answer)
                    pattern = re.compile(f'({escaped_answer})', re.IGNORECASE)
                    highlighted = pattern.sub(
                        r'<span class="highlight-dodge" title="Potential question dodging">\1</span>',
                        highlighted
                    )
        
        return highlighted
    
    def generate_summary_stats(self, analysis_result):
        """
        Generate summary statistics from analysis.
        """
        stats = {
            "confidence_score": analysis_result.get("confidence_score", 0),
            "risk_level": analysis_result.get("risk_level", "UNKNOWN"),
            "hedging_count": len(analysis_result.get("hedging_language", [])),
            "concerns_count": len(analysis_result.get("key_concerns", [])),
            "dodged_questions": len(analysis_result.get("question_dodging", [])),
            "positive_signals": len(analysis_result.get("positive_signals", []))
        }
        
        # Calculate overall health score (0-100)
        health_score = stats["confidence_score"]
        health_score -= stats["hedging_count"] * 2
        health_score -= stats["concerns_count"] * 5
        health_score -= stats["dodged_questions"] * 3
        health_score = max(0, min(100, health_score))  # Clamp to 0-100
        
        stats["health_score"] = health_score
        
        return stats

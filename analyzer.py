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

Analyze this transcript and identify potential red flags, hedging language, and areas of concern that might indicate:
- Management uncertainty or lack of confidence
- Evasive answers to analyst questions
- Vague or non-committal language
- Potential risks being downplayed
- Inconsistencies or contradictions

Please provide your analysis in the following JSON format. IMPORTANT: Escape all quotes inside string values using backslashes (\\"):

{{
  "confidence_score": <0-100, where 100 is most confident/transparent and 0 is most concerning/evasive>,
  "overall_assessment": "<2-3 sentence summary of management credibility and transparency>",
  "hedging_language": [
    {{
      "phrase": "<the hedging phrase found>",
      "context": "<surrounding sentence for context>",
      "severity": "<low|medium|high>",
      "reason": "<why this is a red flag>"
    }}
  ],
  "key_concerns": [
    {{
      "concern": "<title of the concern>",
      "description": "<detailed explanation>",
      "evidence": "<quote from transcript>",
      "impact": "<potential impact on investors>"
    }}
  ],
  "question_dodging": [
    {{
      "question": "<analyst question>",
      "answer": "<management response>",
      "analysis": "<how they dodged or deflected>"
    }}
  ],
  "positive_signals": [
    "<any transparent or confidence-inspiring moments>"
  ],
  "risk_level": "<LOW|MEDIUM|HIGH>"
}}

TRANSCRIPT:
{transcript_text}

Remember to be thorough but fair - look for genuine red flags, not normal business language. Focus on patterns that might indicate management is being less than forthcoming. CRITICAL: Always escape quotes in your JSON strings using backslashes."""

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
                try:
                    result = json.loads(json_match.group())
                    logger.info(f"✅ Successfully parsed JSON with keys: {list(result.keys())}")
                    # Add raw response to result
                    result['_raw_response'] = result_text
                except json.JSONDecodeError as e:
                    logger.error(f"❌ JSON parsing failed: {str(e)}")
                    logger.error(f"❌ Error at position {e.pos}: {json_match.group()[max(0, e.pos-50):e.pos+50]}")
                    # Try to fix common JSON issues
                    json_text = json_match.group()
                    
                    # Fix unescaped quotes in strings - more comprehensive approach
                    # Replace quotes that are inside string values but not properly escaped
                    
                    # Find all string values and fix quotes within them
                    def fix_quotes_in_strings(match):
                        content = match.group(1)
                        # Escape any unescaped quotes inside the string
                        fixed_content = content.replace('\\"', '___ESCAPED_QUOTE___')  # Temporarily replace already escaped quotes
                        fixed_content = fixed_content.replace('"', '\\"')  # Escape all quotes
                        fixed_content = fixed_content.replace('___ESCAPED_QUOTE___', '\\"')  # Restore escaped quotes
                        return f'"{fixed_content}"'
                    
                    # Apply the fix to all string values
                    json_text = re.sub(r'"([^"]*(?:\\"[^"]*)*)"', fix_quotes_in_strings, json_text)
                    
                    try:
                        result = json.loads(json_text)
                        logger.info("✅ Successfully parsed JSON after fixing quotes")
                        # Add raw response to result
                        result['_raw_response'] = result_text
                    except Exception as fix_error:
                        logger.warning(f"❌ Could not fix JSON: {fix_error}")
                        result = {
                            "error": "Could not parse analysis - JSON syntax error",
                            "raw_response": result_text,
                            "confidence_score": 50,  # Default fallback
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

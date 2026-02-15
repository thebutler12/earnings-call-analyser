"You are an expert financial analyst reviewing an earnings call transcript for {company_name} ({quarter}). 

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
"""
Sample earnings call transcripts for analysis.
In production, these would be fetched from SEC EDGAR or earnings call providers.
"""

SAMPLE_TRANSCRIPTS = {
    "tech_corp_q4_2024": {
        "company": "TechCorp Inc.",
        "quarter": "Q4 2024",
        "date": "January 28, 2025",
        "transcript": """
OPERATOR: Good afternoon, and welcome to TechCorp's Fourth Quarter 2024 Earnings Conference Call. All participants will be in listen-only mode until the question-and-answer session.

SARAH CHEN, CEO: Thank you for joining us today. I'm pleased to report that Q4 was a strong quarter for TechCorp. Revenue grew 12% year-over-year to $4.2 billion, which we believe demonstrates the strength of our cloud platform.

Our AI division showed promising signs of traction, though it's still early days. We expect to see more meaningful contribution from this segment in the coming quarters, hopefully by mid-2025. The competitive landscape remains challenging, but we think we're well-positioned to compete.

Margins were impacted by higher R&D spending, which we believe is necessary for long-term growth. We're investing heavily in AI capabilities, and while it's difficult to predict exactly when these investments will pay off, we're optimistic about the trajectory.

JOHN MARTINEZ, CFO: Looking at the numbers, operating expenses increased 18% year-over-year, primarily due to headcount additions and infrastructure costs. We expect this trend to continue in Q1 as we scale our AI initiatives.

Free cash flow was $800 million, down from $1.1 billion last year. This was largely anticipated and reflects our strategic investments. We believe this is the right approach for positioning the company for future growth.

For Q1 2025, we're guiding revenue to $4.0-$4.3 billion, which assumes normal seasonality and no major macroeconomic disruptions.

ANALYST QUESTION: Can you provide more specific metrics on AI product adoption? What percentage of customers are actively using these features?

SARAH CHEN: That's a great question. We're seeing good engagement, though we don't break out specific adoption numbers at this time. What I can say is that customer feedback has been positive, and we're encouraged by the early signals. We think the real test will be in the next few quarters as we roll out more advanced capabilities.

ANALYST QUESTION: The margin compression is concerning. When should we expect to see operating leverage return?

JOHN MARTINEZ: We understand the concern. Look, we're in an investment phase, and we believe these investments are critical. It's hard to give a precise timeline, but we expect to see gradual improvement throughout 2025. That said, we're committed to maintaining our investment levels in strategic areas, so the path to margin expansion may be slower than in past cycles.

ANALYST QUESTION: Your largest competitor just announced a major partnership in AI. How does this impact your competitive position?

SARAH CHEN: We're aware of that announcement. Obviously, we can't comment on competitors' strategies. What I'd say is that we have our own partnerships in development, and we feel good about our technology differentiation. The market is large enough for multiple players, and we're focused on executing our own roadmap.

OPERATOR: That concludes our call today. Thank you for joining.
""",
        "key_metrics": {
            "revenue": "$4.2B",
            "growth": "12% YoY",
            "free_cash_flow": "$800M"
        }
    },
    
    "retail_co_q3_2024": {
        "company": "RetailCo",
        "quarter": "Q3 2024",
        "date": "November 5, 2024",
        "transcript": """
OPERATOR: Welcome to RetailCo's Third Quarter 2024 Earnings Call.

MIKE THOMPSON, CEO: Good morning. Q3 was a challenging quarter for RetailCo. Comparable store sales declined 3.2%, which was below our expectations. We're seeing softer consumer spending across most categories, particularly in discretionary items.

We believe the macroeconomic environment remains uncertain, and consumer sentiment appears to be weakening. That said, we're taking aggressive action to address these headwinds.

We've initiated a cost reduction program that we expect will generate $200-$300 million in savings over the next 18 months. This includes store closures, workforce optimization, and supply chain efficiencies.

JENNIFER LI, CFO: Gross margins contracted 150 basis points to 32.1%, driven by increased promotional activity and inventory clearance. We had excess inventory coming into the quarter, which we believe we've now largely worked through.

Inventory levels are down 8% sequentially, which puts us in a better position heading into the holiday season. We expect Q4 to be critical, and we're cautiously optimistic about holiday traffic.

Operating expenses increased 5%, which was higher than we would have liked. We're taking steps to bring this under control, though some costs are difficult to reduce in the near term.

ANALYST QUESTION: Can you walk through your assumptions for Q4 guidance? It seems optimistic given current trends.

MIKE THOMPSON: Sure. Our guidance assumes a modest improvement in consumer spending during the holiday season. We're planning our inventory and promotional calendar accordingly. Obviously, there's uncertainty, but we believe our assumptions are reasonable based on what we're seeing so far.

ANALYST QUESTION: Several competitors have filed for bankruptcy recently. Are you seeing any benefit from their store closures?

MIKE THOMPSON: It's a fair question. We've seen some market share gains in certain regions, though it's hard to quantify precisely. The overall pie is shrinking, so gaining share in a declining market is challenging. We think the consolidation will ultimately be healthy for the industry, but it may take time to play out.

ANALYST QUESTION: Your debt-to-EBITDA ratio is now 3.2x, above your stated comfort range. What's your plan to delever?

JENNIFER LI: Yes, we're focused on this. Our priority is generating cash flow and paying down debt. The cost reduction program should help, and we're exploring asset sales that could accelerate deleveraging. We're committed to getting back within our target range, though the timeline depends on operational performance.

OPERATOR: Thank you all for participating.
""",
        "key_metrics": {
            "comp_sales": "-3.2%",
            "gross_margin": "32.1%",
            "debt_to_ebitda": "3.2x"
        }
    },

    "pharma_inc_q2_2024": {
        "company": "PharmaInc",
        "quarter": "Q2 2024",
        "date": "August 8, 2024",
        "transcript": """
OPERATOR: Welcome to PharmaInc's Second Quarter 2024 Earnings Call.

DR. ELIZABETH RODRIGUEZ, CEO: Thank you for joining us. Q2 was an outstanding quarter for PharmaInc. Total revenue reached $6.8 billion, up 24% year-over-year, driven by strong performance across our oncology portfolio.

Our lead drug, OncoBlock, exceeded $2 billion in quarterly sales, making it one of the fastest-growing oncology therapies in the market. Adoption rates remain strong, and we're seeing expanded usage in earlier-stage patients.

Our pipeline continues to advance. We recently received breakthrough therapy designation for our Alzheimer's candidate, which accelerates our regulatory timeline. We expect to file for approval in late 2025, with potential launch in 2026.

Clinical trial results for our diabetes program will be presented at the ADA conference next month. We're confident in the data and believe it positions us well in a competitive but growing market.

DAVID KIM, CFO: Gross margins expanded to 78%, reflecting favorable product mix and manufacturing efficiencies. R&D spending increased to $1.4 billion as we advance multiple late-stage programs.

Operating cash flow was $3.2 billion, up 32% year-over-year. We're well-capitalized to fund our pipeline and return capital to shareholders. We're increasing our quarterly dividend by 15% and announcing a $5 billion share buyback program.

For full-year 2024, we're raising our revenue guidance to $26-$27 billion, up from previous guidance of $24-$25 billion.

ANALYST QUESTION: Can you discuss the competitive threat from biosimilars to OncoBlock? When do you expect first competition?

DR. RODRIGUEZ: We've been preparing for biosimilar competition for several years. Patent protection extends through 2029 in the US, and we have additional patents that could extend exclusivity further. We have a robust lifecycle management strategy including new formulations and combination therapies that we believe will maintain our competitive position.

ANALYST QUESTION: The Alzheimer's space has seen high-profile failures. What gives you confidence in your candidate?

DR. RODRIGUEZ: That's an important question. Our mechanism of action is differentiated from previous failures. We target a different pathway, and our Phase 2 data showed statistically significant cognitive improvement with a favorable safety profile. Obviously, Phase 3 will be definitive, but we believe we have a strong scientific foundation.

ANALYST QUESTION: You're guiding well above Street estimates. What's driving the upside?

DAVID KIM: Several factors. OncoBlock uptake is exceeding our initial projections, particularly in international markets. We're also seeing better-than-expected performance from our specialty medicines portfolio. The guidance assumes these trends continue for the remainder of the year.

OPERATOR: This concludes today's call. Thank you.
""",
        "key_metrics": {
            "revenue": "$6.8B",
            "growth": "24% YoY",
            "gross_margin": "78%"
        }
    }
}

def get_transcript(key):
    """Get a specific transcript by key"""
    return SAMPLE_TRANSCRIPTS.get(key)

def get_all_transcripts():
    """Get all available transcripts"""
    return SAMPLE_TRANSCRIPTS

def get_transcript_list():
    """Get list of available transcripts for selection"""
    return [
        {
            "key": key,
            "company": data["company"],
            "quarter": data["quarter"],
            "date": data["date"]
        }
        for key, data in SAMPLE_TRANSCRIPTS.items()
    ]

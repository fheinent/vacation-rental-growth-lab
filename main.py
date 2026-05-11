import os
import re
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx
from anthropic import Anthropic

# Initialize FastAPI and Anthropic
app = FastAPI()
client = Anthropic()

class AnalysisRequest(BaseModel):
    url: str

class AnalysisResponse(BaseModel):
    experiments: list
    quick_wins: list
    champion_brief: str
    page_title: str
    page_description: str

def clean_html(html: str) -> str:
    """Remove scripts, styles, and extra whitespace."""
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'\s+', ' ', html).strip()
    return html[:8000]  # Limit to 8k chars

async def fetch_page(url: str) -> str:
    """Fetch and clean HTML from URL."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return clean_html(response.text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

def parse_experiments(response_text: str) -> list:
    """Parse Claude's experiment output into structured list."""
    experiments = []
    sections = response_text.split("Experiment #")

    for section in sections[1:]:  # Skip the preamble
        lines = section.strip().split("\n")
        if len(lines) >= 3:
            exp_num = lines[0].split(":")[0].strip() if ":" in lines[0] else ""
            title = lines[1] if len(lines) > 1 else ""

            # Extract ICE scores
            ice_match = re.search(r"Ice Score.*?(\d+\.?\d*)", section)
            ice = float(ice_match.group(1)) if ice_match else 0

            impact_match = re.search(r"Impact.*?(\d+)", section)
            impact = int(impact_match.group(1)) if impact_match else 0

            confidence_match = re.search(r"Confidence.*?(\d+)", section)
            confidence = int(confidence_match.group(1)) if confidence_match else 0

            ease_match = re.search(r"Ease.*?(\d+)", section)
            ease = int(ease_match.group(1)) if ease_match else 0

            experiments.append({
                "number": exp_num,
                "title": title.replace("Title:", "").strip(),
                "ice_score": ice,
                "impact": impact,
                "confidence": confidence,
                "ease": ease,
                "hypothesis": section.split("Hypothesis:")[1].split("\n")[0].strip() if "Hypothesis:" in section else "",
                "metric": section.split("Success Metric:")[1].split("\n")[0].strip() if "Success Metric:" in section else "",
                "sample_size": re.search(r"Sample size.*?(\d+[,\d]*)", section).group(1) if re.search(r"Sample size.*?(\d+[,\d]*)", section) else ""
            })

    return sorted(experiments, key=lambda x: x["ice_score"], reverse=True)[:5]

def parse_quick_wins(response_text: str) -> list:
    """Extract quick wins from Claude response."""
    quick_wins = []
    if "Quick Wins" in response_text or "immediate changes" in response_text:
        section = response_text.split("Quick Wins")[1] if "Quick Wins" in response_text else response_text.split("immediate changes")[1]
        lines = section.split("\n")
        for i, line in enumerate(lines[:6]):
            if line.strip() and not line.startswith("#"):
                quick_wins.append(line.strip())
    return [w for w in quick_wins if w][:4]

@app.post("/api/analyze")
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    """Analyze a vacation rental landing page for A/B experiment opportunities."""

    # Validate URL
    if not request.url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")

    # Fetch page content
    page_content = await fetch_page(request.url)

    # Prepare Claude prompt with cache
    system_prompt = """You are a growth strategist analyzing vacation rental property management software landing pages.
Your job is to identify high-impact A/B testing opportunities using the ICE (Impact, Confidence, Ease) framework.

For each experiment:
- Impact (1-10): How much will this change conversion?
- Confidence (1-10): How confident are you it will work?
- Ease (1-10): How easy is it to implement?
- ICE Score: (Impact + Confidence + Ease) / 3

Output exactly 5 experiments, ranked by ICE score."""

    user_prompt = f"""Analyze this vacation rental software landing page and generate 5 A/B test hypotheses:

PAGE CONTENT:
{page_content}

For each experiment, provide:
- Experiment #N (1-5)
- Title: [Brief title]
- Ice Score: [X.X]
- Impact: [1-10]
- Confidence: [1-10]
- Ease: [1-10]
- Hypothesis: [What will change and why]
- Success Metric: [How to measure]
- Sample size: [Estimated visitors needed]

Then add a "Quick Wins" section with 3-4 non-test improvements.

Then add "Champion Brief" section with 2-3 sentences on how a Growth Champion would use this roadmap."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        response_text = response.content[0].text

        # Parse response
        experiments = parse_experiments(response_text)
        quick_wins = parse_quick_wins(response_text)

        # Extract champion brief
        champion_brief = ""
        if "Champion Brief" in response_text:
            champion_brief = response_text.split("Champion Brief")[1].split("\n")[1:3]
            champion_brief = "\n".join(champion_brief).strip()

        return AnalysisResponse(
            experiments=experiments,
            quick_wins=quick_wins,
            champion_brief=champion_brief,
            page_title=request.url.split("/")[-1] or "Landing Page",
            page_description=f"Analysis of {request.url[:50]}..."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/")
async def root():
    """Serve the index page."""
    return FileResponse("static/index.html")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# Vacation Rental Growth Lab

An AI-powered tool for analyzing vacation rental landing pages and generating A/B experiment roadmaps using ICE scoring (Impact, Confidence, Ease).

## Features

- **AI-Powered Analysis**: Fetches and analyzes landing page content using Claude Sonnet
- **ICE Framework**: Prioritizes experiments using Impact, Confidence, and Ease scoring
- **Quick Wins**: Identifies non-test improvements
- **Champion Brief**: Provides strategic playbook guidance
- **Prompt Caching**: Uses Anthropic's prompt caching for cost efficiency

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: HTML5, Tailwind CSS (no build step)
- **AI**: Anthropic Claude API (claude-sonnet-4-6)
- **Deployment**: Railway

## Local Development

### Prerequisites
- Python 3.9+
- ANTHROPIC_API_KEY environment variable set

### Setup

```bash
# Clone or download the project
cd vacation-rental-growth-lab

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export ANTHROPIC_API_KEY="your-api-key-here"
# OR create a .env file (not in version control)

# Run the server
python main.py
```

The application will be available at `http://localhost:8000`

## Deployment to Railway

### 1. Prepare Your Code
```bash
git init
git add .
git commit -m "Initial commit"
```

### 2. Connect to Railway
- Go to [railway.app](https://railway.app)
- Create a new project → "Deploy from GitHub" (or "Deploy from Repository")
- Connect your repository

### 3. Set Environment Variables
In Railway dashboard:
1. Go to Variables
2. Add `ANTHROPIC_API_KEY` with your API key
3. Railway will automatically detect `requirements.txt` and `Procfile`

### 4. Deploy
Railway will automatically:
- Install dependencies from `requirements.txt`
- Run the application using the `Procfile` configuration
- Assign a public URL

## API Reference

### POST `/api/analyze`

Analyzes a landing page and returns experiment recommendations.

**Request:**
```json
{
  "url": "https://example.com/landing-page"
}
```

**Response:**
```json
{
  "experiments": [
    {
      "number": "1",
      "title": "Experiment Title",
      "ice_score": 8.3,
      "impact": 9,
      "confidence": 8,
      "ease": 8,
      "hypothesis": "...",
      "metric": "...",
      "sample_size": "1,000"
    }
  ],
  "quick_wins": ["...", "..."],
  "champion_brief": "...",
  "page_title": "Landing Page",
  "page_description": "Analysis of example.com..."
}
```

## How It Works

1. **Page Fetching**: User submits a URL
2. **Content Cleaning**: HTML is cleaned (scripts/styles removed, truncated to 8k chars)
3. **AI Analysis**: Claude analyzes the page and generates 5 A/B test hypotheses
4. **Parsing**: Response is structured into experiments, quick wins, and strategy
5. **Scoring**: Experiments ranked by ICE score
6. **Display**: Results shown in tabbed interface

## File Structure

```
vacation-rental-growth-lab/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Procfile               # Railway/Heroku process definition
├── static/
│   └── index.html        # Frontend UI
└── README.md             # This file
```

## Cost Estimate

- **API Calls**: ~$0.02-0.05 per analysis (Claude Sonnet with caching)
- **Hosting**: Railway free tier or $5-20/month for paid plans
- **Monthly Cost**: < €10 for moderate usage

## Environment Variables

- `ANTHROPIC_API_KEY` (required): Your Anthropic API key
- `PORT` (optional): Server port, defaults to 8000

## License

MIT

# Quick Deployment Guide to Railway

## ⚡ 5-Minute Setup

### Step 1: Clone/Upload to GitHub
```bash
# If not already in git
git init
git add .
git commit -m "Vacation Rental Growth Lab - AI experiment generator"

# Push to GitHub (create a repo first at github.com/new)
git remote add origin https://github.com/YOUR_USERNAME/vacation-rental-growth-lab.git
git push -u origin main
```

### Step 2: Deploy to Railway
1. Go to https://railway.app
2. Click "Create a new project"
3. Select "Deploy from GitHub repo"
4. Authorize GitHub and select your `vacation-rental-growth-lab` repo
5. Railway will automatically detect `requirements.txt` and `Procfile`
6. Wait for deployment (~1-2 min)

### Step 3: Add Environment Variables
In Railway dashboard:
1. Click on your project
2. Go to "Variables" tab
3. Add:
   - Key: `ANTHROPIC_API_KEY`
   - Value: Your API key from https://console.anthropic.com
4. Click "Save"
5. Railway will redeploy automatically

### Step 4: Get Your Public URL
1. In Railway, go to "Deployments"
2. Find the "Domains" section
3. You'll see a URL like: `https://vacation-rental-growth-lab-production.up.railway.app`
4. Click the URL to test it loads

### Step 5: Test the Tool
1. Open the URL
2. The default URL (Lodgify) should be pre-filled
3. Click "Generate Experiment Roadmap"
4. Wait 15-30 seconds for Claude to analyze
5. You should see 5 experiments with ICE scores

## 🎥 Record a Demo Video

Once deployed:
1. Open the public URL in a fresh browser
2. Use ScreenFlow or similar to record 60 seconds:
   - Show the input with Lodgify URL (5 sec)
   - Click "Generate Experiment Roadmap" (5 sec)
   - Show loading state (5 sec)
   - Results screen: scroll through experiments (20 sec)
   - Show Quick Wins tab (10 sec)
   - Show Champion Brief tab (10 sec)
3. Save as `demo-vacation-rental-growth-lab.mp4`

## 📝 How to Mention in Interview

**In conversation with Lola:**

> "I spent the weekend diving into the Lodgify domain — their landing pages, what they optimize for. And I built a tool that shows how I'd approach this: it analyzes a vacation rental software landing page and generates an A/B experiment roadmap using the ICE framework.
>
> Here's what it does: [show URL or demo]. You paste a URL, Claude analyzes the content, and you get 5 prioritized experiments with impact/confidence/ease scores, plus quick wins and a champion playbook.
>
> It demonstrates the three things this role needs — experimentation thinking, AI infrastructure, and how I'd build a champion network. It's functional, not a mockup."

## 🔧 Troubleshooting

**"Deploy is stuck"**
- Check GitHub Actions in your repo
- Railway should auto-detect `Procfile` and `requirements.txt`
- If not, manually set build command: `pip install -r requirements.txt`

**"500 Error on /api/analyze"**
- Check that `ANTHROPIC_API_KEY` is set in Railway Variables
- Redeploy after adding the key: Railway menu → "Redeploy"

**"Can't fetch the URL"**
- Some websites block automated requests
- The tool will fail gracefully with an error message
- Try with https://example.com first to test

**"Response is slow (>30 sec)"**
- Claude is processing — this is normal for first request
- Subsequent requests with same URL will be faster due to prompt caching
- Railway free tier has slower specs, so expect 15-30 seconds

## 💰 Cost

- Railway free tier: $5/month credit (enough for this demo)
- Claude API: ~$0.02-0.05 per analysis
- Total monthly cost: < €5 if used moderately

## 📚 Next Steps After Deploy

1. Test with a few different URLs
2. Record the 60-second demo
3. Keep the public URL handy for the interview
4. Have the GitHub repo link ready if they ask to see code
5. Mention it naturally in the interview as evidence of domain learning

---

**Time to deploy: ~5 minutes**  
**Time to test: ~2 minutes**  
**Time to record demo: ~10 minutes**  
**Total prep time: ~20 minutes**

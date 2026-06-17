# Deploying to Vercel + Vercel Postgres

## Prerequisites
- [Vercel account](https://vercel.com) (free)
- [Node.js](https://nodejs.org) installed (for Vercel CLI)
- [Git](https://git-scm.com) installed

---

## Step 1 — Install Vercel CLI
Open a terminal (PowerShell or Git Bash) and run:
```bash
npm install -g vercel
```

---

## Step 2 — Push project to GitHub
```bash
cd C:\Users\ASUS\Desktop\nepal_education_platform
git init
git add .
git commit -m "Initial commit — Nepal Education Platform"
```
Then create a new repo on GitHub and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/nepal_education_platform.git
git push -u origin main
```

---

## Step 3 — Deploy to Vercel
```bash
vercel
```
Follow the prompts:
- **Set up and deploy?** → Y
- **Which scope?** → your account
- **Link to existing project?** → N
- **Project name?** → nepal-education-platform
- **Directory?** → ./  (press Enter)
- **Override settings?** → N

Vercel will deploy and give you a URL like `https://nepal-education-platform.vercel.app`

---

## Step 4 — Add Vercel Postgres

1. Go to your project at **vercel.com/dashboard**
2. Click **Storage** → **Create Database** → **Postgres**
3. Name it `nepal-edu-db`, click **Create**
4. Click **Connect to Project** → select your project
5. Vercel automatically adds `DATABASE_URL` to your project's environment variables

---

## Step 5 — Set Environment Variables

In your Vercel project → **Settings** → **Environment Variables**, add:

| Variable | Value |
|---|---|
| `SECRET_KEY` | any long random string |
| `JWT_SECRET_KEY` | any long random string |
| `AI_PROVIDER` | `openai` or `gemini` |
| `OPENAI_API_KEY` | your OpenAI key (optional) |
| `GEMINI_API_KEY` | your Gemini key (optional) |
| `FLASK_ENV` | `production` |

> `DATABASE_URL` is added automatically by Vercel Postgres — do NOT add it manually.

---

## Step 6 — Run the Database Schema

After deployment, run the schema against your Vercel Postgres:

1. In Vercel dashboard → **Storage** → your database → **Query**
2. Paste the contents of `schema_postgres.sql` and click **Run**

OR via the CLI (install `psql` first):
```bash
psql $DATABASE_URL -f schema_postgres.sql
```

---

## Step 7 — Redeploy
```bash
vercel --prod
```

Your app is live at: `https://nepal-education-platform.vercel.app`

---

## Important Notes

| Feature | Status on Vercel Free |
|---|---|
| Flask routes | Works |
| Vercel Postgres | Works (500 MB free) |
| AI exam generation | Works (needs API key) |
| File uploads | Temporary only (`/tmp`) — use S3 for permanent |
| OCR (Tesseract) | Not available on Vercel — needs Railway/Render |
| Background jobs (Celery) | Not available — use Vercel Cron Jobs instead |

### For full OCR support:
If you need OCR answer sheet evaluation, deploy to **Railway** instead:
```bash
railway login
railway init
railway up
```

---

## Local Development with Postgres
```bash
# Install deps
pip install -r requirements.txt

# Start local Postgres (or use the Vercel Postgres connection string)
# Edit .env and set DATABASE_URL or DB_* variables

# Run the schema
psql -U postgres -d nepal_edu_platform -f schema_postgres.sql

# Start Flask
python app.py
# Open: http://127.0.0.1:5000
```

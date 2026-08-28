# ZxZone-HK-MLB — Heroku Optimized Telegram Mirror & Leech Bot

The Most Powerful Heroku-Focused Mirror & Leech Bot with 100+ Features, Stealth Protection, and 24/7 Uptime.

---

## Overview

ZxZone-HK-MLB is specifically optimized for Heroku deployment. It includes stealth protection to avoid detection, anti-ban system, keep-alive technology, and all powerful features for mirroring and leeching.

---

## Features

### Download System
- Direct Links, Torrents, Magnets
- M3U8 Streams, Icc.Tv, Viking Files
- Mega, Gofile, Pixeldrain
- Google Drive, YouTube
- JDownloader (1000+ sites)

### Upload System
- Telegram (Document/Video/Audio)
- Rclone (50+ clouds)
- Google Drive
- 1080p HD Thumbnail Auto Generation
- Auto Split (2GB/4GB)

### Video Tools
- Video Merge, Convert, Encode
- Multi-Resolution, HardSub, Watermark
- Audio Extract, Video Compress

### Settings
- 15 Pages Config Variables
- 5 Pages Aria2 Settings
- Private Files Management
- JD Account Management

### Heroku Stealth Protection
- Detection Evasion
- Anti-Ban System
- Process Rotation
- Random User Agents
- Header Hiding
- Rate Limit Protection

### Heroku Optimization
- 24/7 Keep Alive
- Auto Restart
- Memory Optimizer
- Smart Cache
- Lazy Loading
- Speed Booster

---

## Heroku Deploy Guide

### Method 1: GitHub Actions (Recommended)

1. Go to your GitHub repo
2. Click on **Actions** tab
3. Select **"Deploy ZxZone-HK-MLB to Heroku"**
4. Click **"Run workflow"** button
5. Fill in the inputs:
   - HEROKU_APP_NAME: Your app name (e.g., zxzonemlb)
   - HEROKU_API_KEY: From Heroku account settings
   - HEROKU_EMAIL: Your Heroku email
   - BOT_TOKEN: From @BotFather
   - OWNER_ID: Your Telegram ID
   - API_ID: From my.telegram.org
   - API_HASH: From my.telegram.org
   - DATABASE_URL: MongoDB connection string
6. Click **"Run workflow"**
7. Wait for deployment to complete

### Method 2: Heroku CLI

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Set config vars
heroku config:set BOT_TOKEN=your_token
heroku config:set API_ID=your_api_id
heroku config:set API_HASH=your_api_hash
heroku config:set OWNER_ID=your_id
heroku config:set DATABASE_URL=your_mongodb_url

# Deploy
git push heroku main

# Start web dyno
heroku ps:scale web=1

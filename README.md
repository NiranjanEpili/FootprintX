# FootprintX Bot

A Telegram bot for security reconnaissance and domain information gathering.

## Features
- DNS Record Analysis
- WHOIS Information
- SSL Certificate Details
- PDF Report Generation

## Setup
1. Clone the repository
2. Copy `.env.example` to `.env`
3. Get your Telegram Bot Token from @BotFather
4. Add your token to `.env` file
5. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Deployment Instructions

### Local Development
1. Copy `.env.example` to `.env`
2. Add your development bot token to `.env`
3. Install requirements and run locally

### Railway Deployment Guide

1. **Prepare Your Repository**
   - Make sure your bot token is removed from `.env`
   - Ensure `.gitignore` is properly configured
   - Push your code to a GitHub repository

2. **Railway Setup**
   - Go to [Railway.app](https://railway.app/)
   - Sign in with your GitHub account
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your FootprintX repository

3. **Configure Environment Variables**
   - In your Railway project, go to "Variables"
   - Add the following variables:
     ```
     BOT_TOKEN=your_production_bot_token
     HIBP_API_KEY=your_hibp_api_key
     DEBUG=False
     ```

4. **Deploy**
   - Railway will automatically deploy your bot
   - Check deployment logs for any errors
   - Bot should start running automatically

5. **Verify Deployment**
   - Test your bot on Telegram
   - Check if all commands are working
   - Monitor logs in Railway dashboard

### Troubleshooting
- If bot doesn't respond, check Railway logs
- Ensure environment variables are set correctly
- Verify your bot token is valid

### Security Notes
- Never commit `.env` file
- Keep production tokens secure
- Use different bot tokens for development and production
- Railway environment variables override local .env file

## Environment Variables
Required:
- `BOT_TOKEN`: Your Telegram bot token
- `HIBP_API_KEY`: (Optional) HaveIBeenPwned API key
- `DEBUG`: Set to 'True' for debug mode

## Author
- Niranjan

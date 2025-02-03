<div align="center">
  
# 🚀 FootprintX Bot

<img src="https://socialify.git.ci/NiranjanEpili/FootprintX/image?font=Jost&language=1&name=1&owner=1&pattern=Plus&stargazers=1&theme=Dark" width="800px" alt="FootprintX Banner">

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://t.me/Footprintxbot)

### Your All-in-One Security Reconnaissance Assistant 🔍
</div>

## 📖 Complete Setup Guide

### Step 1: Prerequisites
- Python 3.8 or higher
- Telegram account
- Basic command line knowledge

### Step 2: Create Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Start chat and type `/newbot`
3. Follow instructions to:
   - Set bot name (e.g., "FootprintX")
   - Set username (e.g., "FootprintXBot")
4. Save the API token provided by BotFather

### Step 3: Clone & Setup
```bash
# Clone repository
git clone https://github.com/NiranjanEpili/footprintx.git

# Navigate to project
cd footprintx

# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows:
venv\Scripts\activate
# For Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configuration
1. Create environment file:
```bash
cp .env.example .env
```

2. Edit `.env` file:
```env
BOT_TOKEN=your_telegram_bot_token_here
DEBUG=False
```

### Step 5: Run Bot
```bash
python main.py
```

## ✨ Features & Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Initialize bot | `/start` |
| `/scan` | Scan domain | `/scan google.com` |
| `/clear` | Clear chat | `/clear` |

## 🔍 What Can It Scan?

### Domain Information
- 📋 DNS Records (A, AAAA, MX, NS, etc.)
- 📊 WHOIS Information
- 🔒 SSL Certificate Details

### Security Checks
- 🌐 Port Scanning
- 🛡️ Security Headers
- 🔑 SSL/TLS Analysis

### Reports
- 📝 Detailed PDF Reports
- 📊 Visual Representations
- 📤 Instant Delivery

## 🛠️ Development Setup

### Required Tools
- Visual Studio Code or PyCharm
- Git
- Python 3.8+

### Directory Structure
```
footprintx/
├── assets/              # Images and static files
├── bot/                 # Bot core files
│   ├── __init__.py
│   ├── telegram_bot.py
│   └── utils.py
├── services/           # Additional services
│   └── report_generator.py
├── config/            # Configuration files
├── .env.example       # Environment template
├── requirements.txt   # Dependencies
└── main.py           # Entry point
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch
```bash
git checkout -b feature/AmazingFeature
```
3. Commit changes
```bash
git commit -m 'Add AmazingFeature'
```
4. Push to branch
```bash
git push origin feature/AmazingFeature
```
5. Open Pull Request

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.

## 📬 Contact & Support

- Created by [@NiranjanEpili](https://github.com/NiranjanEpili)
- Report bugs: [Issues](https://github.com/NiranjanEpili/footprintx/issues)
- Join discussion: [Discussions](https://github.com/NiranjanEpili/footprintx/discussions)

<div align="center">
  
### Made with 💖 by Niranjan

[**Star ⭐ this repo if you found it helpful!**](https://github.com/NiranjanEpili/footprintx)
</div>

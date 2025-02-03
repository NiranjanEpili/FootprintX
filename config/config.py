import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found. Please set it in .env file or environment variables")

# API Keys and Configurations
HIBP_API_KEY = os.getenv('HIBP_API_KEY', '')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

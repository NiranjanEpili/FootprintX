import telebot
import dns.resolver
import whois
import requests
import socket
import nmap
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from email_validator import validate_email, EmailNotValidError
from bot.utils import *
import io
from datetime import datetime
from services.report_generator import ReportGenerator
from telebot.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import logging
import time
import sys
import os
from config.config import BOT_TOKEN, DEBUG

# Initialize bot with token from config
bot = telebot.TeleBot(BOT_TOKEN)

# Configure logging for Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def clean_domain(domain):
    parsed = urlparse(domain)
    return parsed.netloc if parsed.netloc else parsed.path.strip('/')

# Create keyboard markup
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton('/start'), KeyboardButton('/scan'))
    keyboard.row(KeyboardButton('/clear'))
    return keyboard

def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔍 Start Scanning", callback_data="start_scan"),
        InlineKeyboardButton("❌ Clear Chat", callback_data="clear_chat"),
        InlineKeyboardButton("ℹ️ Help", callback_data="help")
    )
    return keyboard

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🌟 *Welcome to FootprintX Bot!* 🌟

I'm your security reconnaissance assistant. I can help you gather information about any domain.

*Owner:* Niranjan
*Version:* 1.0

*Available Commands:*
📍 /start - Show this welcome message
🔍 /scan - Start domain scanning
🗑️ /clear - Clear chat history

Click the buttons below or use commands to get started!
    """
    bot.reply_to(
        message, 
        welcome_text,
        parse_mode='Markdown',
        reply_markup=get_inline_keyboard()
    )
    bot.send_message(
        message.chat.id,
        "Use the menu below for quick access to commands:",
        reply_markup=get_main_keyboard()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "start_scan":
        bot.answer_callback_query(call.id)
        msg = bot.send_message(
            call.message.chat.id,
            "🌐 Please enter the domain you want to scan:\n\n"
            "Example: google.com"
        )
        bot.register_next_step_handler(msg, process_domain_step)
    elif call.data == "clear_chat":
        bot.answer_callback_query(call.id)
        try:
            # Delete the message with the clear button
            bot.delete_message(call.message.chat.id, call.message.message_id)
            
            # Delete previous messages
            deleted = delete_messages(call.message.chat.id, call.message.message_id)
            
            # Send and then delete confirmation
            confirm_msg = bot.send_message(
                call.message.chat.id,
                f"🗑️ Deleted {deleted} messages\n✨ Chat cleared! Type /start to begin again.",
                reply_markup=get_main_keyboard()
            )
            
            # Delete confirmation after 3 seconds
            time.sleep(3)
            try:
                bot.delete_message(call.message.chat.id, confirm_msg.message_id)
            except:
                pass
                
        except Exception as e:
            error_msg = bot.send_message(
                call.message.chat.id,
                "❌ Could not delete all messages. Please clear chat manually or try again."
            )
            time.sleep(3)
            try:
                bot.delete_message(call.message.chat.id, error_msg.message_id)
            except:
                pass
    elif call.data == "help":
        bot.answer_callback_query(call.id)
        help_text = """
*How to use FootprintX Bot:*

1. Click "Start Scanning" or use /scan
2. Enter the domain name when prompted
3. Wait for the complete security report

*Tips:*
• Enter domain without http/https
• Example: google.com
• Use /clear to clean the chat
        """
        bot.send_message(
            call.message.chat.id, 
            help_text,
            parse_mode='Markdown'
        )

def process_domain_step(message):
    try:
        domain = clean_domain(message.text)
        if domain:
            bot.reply_to(
                message, 
                f"🔍 Starting comprehensive scan for *{domain}*...\n"
                "Please wait while I gather information.",
                parse_mode='Markdown'
            )
            full_scan_process(message, domain)
        else:
            bot.reply_to(
                message,
                "⚠️ Invalid domain format. Please try again with a valid domain."
            )
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Full scan command
@bot.message_handler(commands=['scan'])
def scan_command(message):
    msg = bot.reply_to(
        message,
        "🌐 Please enter the domain you want to scan:\n\n"
        "Example: google.com"
    )
    bot.register_next_step_handler(msg, process_domain_step)

def delete_messages(chat_id, message_id):
    """Delete messages in bulk"""
    deleted = 0
    for i in range(message_id, 1, -1):
        try:
            bot.delete_message(chat_id, i)
            deleted += 1
            # Stop if we've deleted a significant number of messages
            if deleted >= 100:
                break
        except Exception as e:
            continue
    return deleted

@bot.message_handler(commands=['clear'])
def clear_command(message):
    try:
        # Delete the clear command message first
        bot.delete_message(message.chat.id, message.message_id)
        
        # Delete previous messages
        deleted = delete_messages(message.chat.id, message.message_id)
        
        # Send and then delete confirmation
        confirm_msg = bot.send_message(
            message.chat.id,
            f"🗑️ Deleted {deleted} messages\n✨ Chat cleared! Type /start to begin again.",
            reply_markup=get_main_keyboard()
        )
        
        # Delete confirmation message after 3 seconds
        time.sleep(3)
        try:
            bot.delete_message(message.chat.id, confirm_msg.message_id)
        except:
            pass
            
    except Exception as e:
        error_msg = bot.reply_to(
            message, 
            "❌ Could not delete all messages. Please clear chat manually or try again."
        )
        # Delete error message after 3 seconds
        time.sleep(3)
        try:
            bot.delete_message(message.chat.id, error_msg.message_id)
        except:
            pass

def full_scan_process(message, domain):
    """Perform the actual scanning process"""
    try:
        results = {}
        
        # DNS Records
        try:
            dns_results = get_dns_records(domain)
            if isinstance(dns_results, dict) and dns_results:
                dns_text = "📋 DNS Records:\n"
                for record_type, records in dns_results.items():
                    dns_text += f"\n{record_type} Records:\n"
                    for record in records:
                        dns_text += f"• {record}\n"
                bot.reply_to(message, dns_text[:4000])
                results['DNS Information'] = dns_results
        except Exception as e:
            bot.reply_to(message, f"❌ DNS lookup error: {str(e)}")
            results['DNS Information'] = {'error': str(e)}
        
        # WHOIS Info
        try:
            whois_info = whois.whois(domain)
            if whois_info:
                whois_text = "📑 WHOIS Information:\n"
                for key, value in whois_info.items():
                    if value and key not in ['status', 'emails']:
                        whois_text += f"\n{key}: {value}"
                bot.reply_to(message, whois_text[:4000])
                results['WHOIS Information'] = whois_info
        except Exception as e:
            bot.reply_to(message, f"❌ WHOIS lookup error: {str(e)}")
            results['WHOIS Information'] = {'error': str(e)}
        
        # SSL Certificate
        try:
            ssl_info = get_ssl_info(domain)  # Changed from get_ssl_certificate_info to get_ssl_info
            if ssl_info:
                ssl_text = "🔒 SSL Certificate Information:\n"
                for key, value in ssl_info.items():
                    ssl_text += f"\n{key}: {value}"
                bot.reply_to(message, ssl_text[:4000])
                results['SSL Certificate'] = ssl_info
        except Exception as e:
            bot.reply_to(message, f"❌ SSL certificate error: {str(e)}")
            results['SSL Certificate'] = {'error': str(e)}
        
        # Generate PDF Report
        report_data = generate_report_data(domain, results)
        report_gen = ReportGenerator()
        pdf_buffer = io.BytesIO()
        report_gen.create_pdf(report_data, pdf_buffer)
        pdf_buffer.seek(0)
        
        # Send PDF report - simplified format
        bot.send_document(
            message.chat.id,
            pdf_buffer,
            visible_file_name=f"footprint_report_{domain}.pdf",
            caption="📊 Here's your detailed security report"
        )
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error during scan: {str(e)}")

# Individual command handlers
@bot.message_handler(commands=['dns'])
def dns_command(message):
    try:
        domain = message.text.split()[1]
        clean_domain_name = clean_domain(domain)
        dns_results = get_dns_records(clean_domain_name)
        if dns_results:
            dns_text = "📋 DNS Records:\n"
            for record_type, records in dns_results.items():
                dns_text += f"\n{record_type} Records:\n"
                for record in records:
                    dns_text += f"• {record}\n"
            bot.reply_to(message, dns_text)
        else:
            bot.reply_to(message, "❌ No DNS records found")
    except IndexError:
        bot.reply_to(message, "⚠️ Please provide a domain name. Example: /dns example.com")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Add other command handlers similarly for whois, ssl, ports, etc.
# ...existing command handlers...

def run_bot():
    while True:
        try:
            logger.info("Bot starting...")
            print("Bot started...")
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            logger.error(f"Bot crashed: {e}")
            print(f"Error: {e}")
            time.sleep(10)  # Wait before retrying
            continue

def main():
    try:
        run_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()

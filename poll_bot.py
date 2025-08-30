#!/usr/bin/env python3
"""
Catholic_DO_Completorium_Bot - Sends daily Compline polls to a Telegram group chat topic
"""

import os
import sys
import requests
import json
from datetime import datetime


def send_poll():
    """Send a daily Compline poll to the specified Telegram group chat topic."""
    
    # Get configuration from environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    message_thread_id = os.getenv('TELEGRAM_MESSAGE_THREAD_ID')  # Topic ID
    
    if not bot_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN environment variable not set")
        sys.exit(1)
        
    if not chat_id:
        print("❌ Error: TELEGRAM_CHAT_ID environment variable not set")
        sys.exit(1)
    
    # Poll configuration for Catholic_DO_Completorium_Bot
    question = "Grace to you and peace from God our Father and the Lord Jesus Christ. Compline at 10pm today? Zoom link: 'https://nus-sg.zoom.us/j/6925593331'"
    options = [
        "Yes",
        "Not today", 
        "Will confirm later today"
    ]
    
    # Telegram Bot API endpoint
    url = f"https://api.telegram.org/bot{bot_token}/sendPoll"
    
    # Poll parameters
    data = {
        'chat_id': chat_id,
        'question': question,
        'options': json.dumps(options),
        'is_anonymous': False,  # Not anonymous as requested
        'allows_multiple_answers': False,  # Only 1 answer allowed
        'type': 'regular'  # Regular type poll
    }
    
    # Add message thread ID if specified (for topic-specific polls)
    if message_thread_id:
        data['message_thread_id'] = message_thread_id
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        
        result = response.json()
        if result.get('ok'):
            print(f"✅ Catholic_DO_Completorium_Bot: Poll sent successfully!")
            print(f"📊 Question: {question}")
            print(f"📋 Options: {', '.join(options)}")
            if message_thread_id:
                print(f"🧵 Topic ID: {message_thread_id}")
            print(f"🕐 Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"❌ Failed to send poll: {result.get('description', 'Unknown error')}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


def get_chat_info():
    """Helper function to get chat information (useful for setup)."""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN environment variable not set")
        return
    
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        result = response.json()
        if result.get('ok'):
            print("📱 Catholic_DO_Completorium_Bot - Recent chat information:")
            for update in result.get('result', []):
                message = update.get('message', {})
                chat = message.get('chat', {})
                if chat:
                    print(f"Chat ID: {chat.get('id')}")
                    print(f"Chat Title: {chat.get('title', 'N/A')}")
                    print(f"Chat Type: {chat.get('type')}")
                    if message.get('message_thread_id'):
                        print(f"Topic ID: {message.get('message_thread_id')}")
                    print("---")
        
    except Exception as e:
        print(f"❌ Error getting chat info: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--get-chat-info":
        get_chat_info()
    else:
        send_poll()

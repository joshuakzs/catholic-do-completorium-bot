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
    question = "Grace to you and peace from God our Father and the Lord Jesus Christ. Compline at 10pm today? Zoom link: https://nus-sg.zoom.us/j/6925593331"
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


def send_reminder():
    """Send a 9 PM reminder message about Compline."""
    
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
    
    # Reminder message
    message = "Compline is in < 1hour!! Yay! Please confirm whether you are coming in the poll"
    
    # Telegram Bot API endpoint for sending messages
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Message parameters
    data = {
        'chat_id': chat_id,
        'text': message
    }
    
    # Add message thread ID if specified (for topic-specific messages)
    if message_thread_id:
        data['message_thread_id'] = message_thread_id
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        
        result = response.json()
        if result.get('ok'):
            print(f"✅ Catholic_DO_Completorium_Bot: Reminder sent successfully!")
            print(f"💬 Message: {message}")
            if message_thread_id:
                print(f"🧵 Topic ID: {message_thread_id}")
            print(f"🕘 Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"❌ Failed to send reminder: {result.get('description', 'Unknown error')}")
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
    
    # First, check if the bot is working
    me_url = f"https://api.telegram.org/bot{bot_token}/getMe"
    try:
        me_response = requests.get(me_url)
        me_result = me_response.json()
        if me_result.get('ok'):
            bot_info = me_result.get('result', {})
            print(f"🤖 Bot Info: {bot_info.get('first_name')} (@{bot_info.get('username')})")
        else:
            print(f"❌ Bot token error: {me_result.get('description')}")
            return
    except Exception as e:
        print(f"❌ Error checking bot: {e}")
        return
    
    # Get updates
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        result = response.json()
        if result.get('ok'):
            updates = result.get('result', [])
            print(f"\n📱 Found {len(updates)} recent updates:")
            
            if not updates:
                print("\n💡 No recent messages found. To get Chat ID and Topic ID:")
                print("   1. Go to your Telegram group/topic")
                print("   2. Send a message mentioning the bot: @Catholic_DO_Completorium_Bot test")
                print("   3. Run this command again immediately after")
                return
            
            seen_chats = set()
            for update in updates:
                message = update.get('message', {})
                chat = message.get('chat', {})
                if chat and chat.get('id') not in seen_chats:
                    seen_chats.add(chat.get('id'))
                    print(f"\n📨 Chat found:")
                    print(f"   Chat ID: {chat.get('id')}")
                    print(f"   Chat Title: {chat.get('title', 'N/A')}")
                    print(f"   Chat Type: {chat.get('type')}")
                    if message.get('message_thread_id'):
                        print(f"   Topic ID: {message.get('message_thread_id')}")
                    print("   ---")
        else:
            print(f"❌ API Error: {result.get('description')}")
        
    except Exception as e:
        print(f"❌ Error getting chat info: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--get-chat-info":
            get_chat_info()
        elif sys.argv[1] == "--send-reminder":
            send_reminder()
        elif sys.argv[1] == "--send-poll":
            send_poll()
        else:
            print("Usage: python poll_bot.py [--get-chat-info|--send-reminder|--send-poll]")
            print("  --get-chat-info: Get chat and topic information")
            print("  --send-reminder: Send 9 PM reminder message")
            print("  --send-poll: Send daily poll (default)")
            sys.exit(1)
    else:
        # Default action is to send poll
        send_poll()

# Catholic_DO_Completorium_Bot

A Telegram bot that automatically sends daily Compline polls to a group chat topic at 10 AM Singapore time.

## Features

- 🕐 Sends daily polls at 10 AM Singapore time via GitHub Actions
- 🕘 Sends reminder messages at 9 PM Singapore time (1 hour before Compline)
- 📊 Sends non-anonymous polls with single-answer selection
- 🧵 Supports Telegram group topics/threads
- ⛪ Customized for Catholic Compline prayer invitations

## Poll Details

**Question:** "Grace to you and peace from God our Father and the Lord Jesus Christ. Compline at 10pm today? Zoom link: 'https://nus-sg.zoom.us/j/6925593331'"

**Options:**
- Yes
- Not today
- Will confirm later today

## Reminder Message

**9 PM Message:** "Compline is in < 1hour!! Yay! Please confirm whether you are coming in the poll"

## Setup Instructions

### 0. Development Setup (Optional - for local testing)

If you want to test the bot locally before deploying:

```bash
# Clone/download this repository
git clone <your-repo-url>
cd telegram-poll-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 1. Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Follow the prompts to name your bot: `Catholic_DO_Completorium_Bot`
4. Save the bot token (it looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Get Your Group Chat ID and Topic ID

1. Add your bot to the Telegram group
2. Give the bot admin permissions
3. If using a topic, navigate to the specific topic where you want polls sent
4. Send a message in the group/topic mentioning your bot (e.g., `@Catholic_DO_Completorium_Bot hello`)

Then run locally to get the chat information:
```bash
# Set your bot token temporarily
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
python poll_bot.py --get-chat-info
```

This will show you the Chat ID and Topic ID (if applicable).

### 3. Fork and Configure GitHub Repository

1. Fork this repository to your GitHub account
2. Go to your forked repository's Settings → Secrets and variables → Actions
3. Add the following repository secrets:

   - `TELEGRAM_BOT_TOKEN`: Your bot token from step 1
   - `TELEGRAM_CHAT_ID`: The chat ID from step 2
   - `TELEGRAM_MESSAGE_THREAD_ID`: The topic ID from step 2 (optional, leave empty if sending to main chat)

### 4. Enable GitHub Actions

1. Go to the Actions tab in your GitHub repository
2. If Actions are disabled, click "I understand my workflows, go ahead and enable them"
3. The workflow will now run automatically at 10 AM Singapore time daily

### 5. Test the Bot

You can test the bot manually by:

1. Going to Actions tab → "Daily Compline Poll" workflow
2. Click "Run workflow" to trigger it manually
3. Check the logs to see if the poll was sent successfully

## Local Testing

To test locally before deploying (using virtual environment):

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
export TELEGRAM_MESSAGE_THREAD_ID="your_topic_id"  # Optional

# Send a test poll (default action)
python poll_bot.py
# or explicitly:
python poll_bot.py --send-poll

# Send a test reminder message
python poll_bot.py --send-reminder

# Get chat information
python poll_bot.py --get-chat-info

# Deactivate virtual environment when done
deactivate
```

## Schedule

The bot runs twice daily:

### Daily Poll
- **10:00 AM Singapore Time (UTC+8)**
- **2:00 AM UTC**

### Reminder Message
- **9:00 PM Singapore Time (UTC+8)**
- **1:00 PM UTC**

## Troubleshooting

### Common Issues

1. **"Chat not found" error**: Make sure the bot is added to the group and has proper permissions
2. **"Forbidden" error**: The bot needs admin permissions or at least permission to send messages
3. **No polls appearing**: Check if `TELEGRAM_MESSAGE_THREAD_ID` is correct for your topic

### Checking Logs

1. Go to GitHub Actions in your repository
2. Click on the latest workflow run
3. Expand the "Send Compline Poll" step to see detailed logs

## File Structure

```
telegram-poll-bot/
├── .github/
│   └── workflows/
│       ├── daily-compline-poll.yml    # GitHub Actions workflow for 10 AM polls
│       └── compline-reminder.yml      # GitHub Actions workflow for 9 PM reminders
├── poll_bot.py                        # Main bot script
├── requirements.txt                    # Python dependencies
├── .gitignore                         # Git ignore file
└── README.md                          # This file
```

## Customization

To modify the poll question, options, or schedule:

1. Edit `poll_bot.py` for question/options changes
2. Edit `.github/workflows/daily-compline-poll.yml` for schedule changes
3. Commit and push your changes

## Support

If you encounter issues:
1. Check the GitHub Actions logs
2. Verify your bot token and chat IDs
3. Ensure the bot has proper permissions in your Telegram group

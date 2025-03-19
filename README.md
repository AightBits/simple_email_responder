# Email LLM Responder

## Description

A simple Python script that polls an email inbox for unread messages, retrieves their contents, sends them to an LLM for processing via an OpenAI-compatible API, and replies with the generated response. The script runs continuously, checking for new emails at regular intervals.

## How It Works

1. **Email Retrieval:**
   - Connects to an IMAP server and fetches unread emails from the inbox.
   - Extracts the sender, subject, and body of each email.

2. **Processing via LLM:**
   - Sends the email content to an OpenAI-compatible API.
   - Optionally includes a system prompt to guide responses.
   - Receives the generated response from the model.

3. **Replying to Emails:**
   - Uses an SMTP server to send the AI-generated response back to the original sender.

4. **Polling Loop:**
   - The script runs indefinitely, checking for new emails every 60 seconds.
   - Handles interruptions gracefully and logs errors.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/email_llm_responder.git
   cd email_llm_responder
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # or
   venv\Scripts\activate     # On Windows
   pip install -r requirements.txt
   ```

## Configuration

Edit the script to set your email and API credentials:

```python
IMAP_SERVER = "imap.example.com"
SMTP_SERVER = "smtp.example.com"
EMAIL_ACCOUNT = "your_email@example.com"
EMAIL_PASSWORD = "your_password"
LLM_API_URL = "https://api.openai.com/v1/chat/completions"
LLM_API_KEY = ""  # Optional API key
SYSTEM_PROMPT = "You are a helpful AI assistant. Keep responses concise and professional."
MODEL = ""  # Optional model
```

## Usage

1. **Start the script:**
   ```bash
   python email_responder.py
   ```

2. **Behavior:**
   - The script continuously checks for new emails.
   - If new emails are found, they are processed and replied to automatically.
   - If no new emails are found, it sleeps for 60 seconds before checking again.

## Example Workflow

```plaintext
$ python email_responder.py
Checking for new emails...
Processing email from alice@example.com with subject: Meeting Update
Replied to alice@example.com with: "Thanks for the update! Looking forward to it."
Sleeping for 60 seconds...
```

## License

This project is licensed under the Apache 2.0.

# Chatbot Boilerplate with Google Auth and Stripe

This repository provides a foundation for building sophisticated chatbot applications using Streamlit, leveraging the power of Google's Vertex AI for natural language processing and integrating secure authentication with Google and Stripe for subscription management.

> ⚠️ **DISCLAIMER**: This boilerplate is for experimental and educational purposes only. It is not intended for production use. Use at your own risk.

## Features:

- **Chat Interface:** A user-friendly Streamlit interface for interacting with your chatbot.
- **Google Authentication:** Secure access through Google OAuth2, allowing users to log in with their Google accounts.
- **Stripe Subscriptions:** Integration of Stripe, enabling paid access to your chatbot.
- **Customizable Chatbot Logic:**  Connect own chatbot models from LM Studio or utilize pre-trained models from Vertex AI.

## Prerequisites

Before running the application, you'll need:

- Python 3.9+
- Google Cloud Platform account with Vertex AI API access
- Google OAuth2 credentials
- Stripe account for subscription management
- GCP Secret Manager set up for secure credential storage

## Installation

1. Clone the repository:
```bash
git clone https://github.com/julhaas91/boilerplate-chatbot.git
cd boilerplate-chatbot
```

2. Create a virtual environment and install dependencies:
```bash
./taskfile.sh reset_venv_local
```

3. Create a `config.env` file in the project root with the following values:
```
GCP_PROJECT_ID=your-gcp-project-id
GCP_PROJECT_NUMBER=your-gcp-project-number
```

4. Create an `allowed_users.txt` file in the `authentication_paywall` directory with a list of authorized email addresses (one per line).

## Usage

### Run locally
```bash
./taskfile.sh run
```

Or run the Streamlit app directly:
```bash
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501`.

### Deploy remotely
```bash
./taskfile.sh deploy
```

## How It Works

1. **Google Authentication**: Users log in using their Google account
2. **Stripe Subscription Verification**: The system checks if the user has an active subscription
3. **Philosopher Selection**: Users select which philosopher they want to chat with
4. **Conversation**: The AI responds in the style and perspective of the selected philosopher

## Configuration Options

### Philosophers
The application currently supports conversations with:
- Socrates
- Plato
- Aristotle
- Nietzsche
- Kant

### AI Models
The application is configured to use:
- `gemini-1.5-flash` (default)
- `gemini-1.5-pro` (available but not selectable in the UI)

## Deployment

The application is designed to be deployable to Google Cloud Run, with testing and production modes configured via Streamlit secrets.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI capabilities provided by [Google Vertex AI](https://cloud.google.com/vertex-ai)
- Authentication through Google OAuth2 (inspired by [st-paywall](https://github.com/tylerjrichards/st-paywall))
- Subscription management via Stripe (inspired by [st-paywall](https://github.com/tylerjrichards/st-paywall))

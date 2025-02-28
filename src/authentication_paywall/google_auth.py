import os
import asyncio
from typing import Optional

import jwt
import streamlit as st
from dotenv import load_dotenv
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2Token

from .utils_auth import get_secret_value
from .common import logger

load_dotenv("config.env")

GCP_PROJECT_NUMBER = os.getenv("GCP_PROJECT_NUMBER")

try:
    secret_value = get_secret_value(GCP_PROJECT_NUMBER, "PHILOSOPHERS_AUTH_ID_AND_SECRET")
    client_id, client_secret = secret_value.split("/")
except Exception as e:
    logger.error(f"Error: {e}")

testing_mode = st.secrets.get("testing_mode", False)
redirect_url = ("http://localhost:8501/" if testing_mode 
                else "https://boilerplate-chatbot-815648219579.europe-west3.run.app")

client = GoogleOAuth2(client_id=client_id, client_secret=client_secret)


def decode_user(token: str):
    """
    Decode a JWT token without verifying its signature.

    This function takes a JWT token as input and decodes it to extract the payload
    information. The signature verification is skipped, which means the token's
    integrity is not checked. This should be used with caution and only in
    scenarios where signature verification is not required or is handled elsewhere.

    Args:
        token: A string representing the JWT token to be decoded.

    Returns:
        A dictionary containing the decoded payload of the JWT token.
    """
    decoded_data = jwt.decode(jwt=token, options={"verify_signature": False})
    return decoded_data


async def get_authorization_url(client: GoogleOAuth2, redirect_url: str) -> str:
    """
    Get the authorization URL for Google OAuth2 authentication.

    Args:
        client: GoogleOAuth2 client instance.
        redirect_url: URL to redirect to after authentication.

    Returns:
        String containing the authorization URL.
    """
    authorization_url = await client.get_authorization_url(
        redirect_url,
        scope=["email"],
        extras_params={"access_type": "offline"},
    )
    return authorization_url


def markdown_button(
    url: str, text: Optional[str] = None, color="#FD504D", sidebar: bool = True
):
    """
    Create a styled button using markdown.

    Args:
        url: The URL the button will direct to when clicked.
        text: The text to display on the button. Defaults to None.
        color: The background color of the button. Defaults to "#FD504D".
        sidebar: Whether to place the button in the sidebar. Defaults to True.
    """
    markdown = st.sidebar.markdown if sidebar else st.markdown

    markdown(
        f"""
    <a href="{url}" target="_blank">
        <div style="
            display: inline-flex;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: center;
            justify-content: center;
            font-weight: 400;
            padding: 0.25rem 0.75rem;
            border-radius: 0.25rem;
            margin: 0px;
            line-height: 1.6;
            width: auto;
            user-select: none;
            background-color: {color};
            color: rgb(255, 255, 255);
            border: 1px solid rgb(255, 75, 75);
            text-decoration: none;
            ">
            {text}
        </div>
    </a>
    """,
        unsafe_allow_html=True,
    )


async def get_access_token(
    client: GoogleOAuth2, redirect_url: str, code: str
) -> OAuth2Token:
    """
    Get access token using authorization code.

    Args:
        client: GoogleOAuth2 client instance.
        redirect_url: URL used during authorization request.
        code: Authorization code received from OAuth provider.

    Returns:
        OAuth2Token object containing the access token and related information.
    """
    token = await client.get_access_token(code, redirect_url)
    return token


def get_access_token_from_query_params(
    client: GoogleOAuth2, redirect_url: str
) -> OAuth2Token:
    """
    Retrieve and process the access token from query parameters.

    Extracts the authorization code from Streamlit query parameters,
    exchanges it for an access token, and clears the query parameters.

    Args:
        client: GoogleOAuth2 client instance.
        redirect_url: URL used during authorization request.

    Returns:
        OAuth2Token object containing the access token and related information.
    """
    code = st.query_params["code"]
    token = asyncio.run(
        get_access_token(client=client, redirect_url=redirect_url, code=code)
    )
    st.query_params.clear()
    return token


def show_login_button(
    text: Optional[str] = "Login with Google", color="#FD504D", sidebar: bool = True
):
    """
    Display a Google login button.

    Args:
        text: The text to display on the button. Defaults to "Login with Google".
        color: The background color of the button. Defaults to "#FD504D".
        sidebar: Whether to place the button in the sidebar. Defaults to True.
    """
    authorization_url = asyncio.run(
        get_authorization_url(client=client, redirect_url=redirect_url)
    )
    markdown_button(authorization_url, text, color, sidebar)


def get_logged_in_user_email() -> Optional[str]:
    """
    Get the email of the currently logged-in user.

    First checks if the email is stored in the session state. If not,
    attempts to get it from query parameters. If successful, stores
    the email in the session state for future use.

    Returns:
        The email address of the logged-in user, or None if not logged in.
    """
    if "email" in st.session_state:
        return st.session_state.email

    try:
        token_from_params = get_access_token_from_query_params(client, redirect_url)
    except KeyError:
        return None

    user_info = decode_user(token=token_from_params["id_token"])
    st.session_state["email"] = user_info["email"]

    return user_info["email"]

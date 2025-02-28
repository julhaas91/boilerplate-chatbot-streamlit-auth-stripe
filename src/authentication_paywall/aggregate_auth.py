import os
import streamlit as st
from .google_auth import get_logged_in_user_email, show_login_button
from .stripe_auth import is_active_subscriber, redirect_button
from .common import logger


def add_auth(
    login_button_text: str = "Login with Google",
    login_button_color: str = "#FD504D",
    login_sidebar: bool = True,

):
    """
    Handles user authentication and subscription status.

    This function checks if a user is logged in and whether they are an active subscriber.
    If the user is not logged in, it displays a login button. If the user is logged in but
    not a subscriber, it displays a subscription button. It also provides a logout button
    in the sidebar.

    Args:
        login_button_text (str): The text to display on the login button. Defaults to "Login with Google".
        login_button_color (str): The color of the login button. Defaults to "#FD504D".
        login_sidebar (bool): Whether to display the login button in the sidebar. Defaults to True.
    """
    user_email = get_logged_in_user_email()

    if not user_email:
        show_login_button(
            text=login_button_text, color=login_button_color, sidebar=login_sidebar
        )
        st.stop()

    _check_user_authorization(user_email)

    is_subscriber = user_email and is_active_subscriber(user_email)

    logger.info(f"User {user_email} is a subscriber: {is_subscriber}")

    if not is_subscriber:
        redirect_button(
            text="Subscribe now!",
            customer_email=user_email
        )
        st.session_state.user_subscribed = False
        st.stop()
    elif is_subscriber:
        st.session_state.user_subscribed = True

    if st.sidebar.button("Logout", type="primary"):
        del st.session_state.email
        st.rerun()


def _check_user_authorization(user_email):
    """
    Checks if the given user email is authorized to access the page for development purposes.

    This helper function reads a list of authorized user emails from 'allowed_users.txt' 
    located in the same directory as this script. If the user email is not in the list, 
    it displays an error message and stops the execution of the script.

    Args:
        user_email (str): The email of the user to check for authorization.

    Note:
        This function is intended for development purposes only to provide an additional 
        layer of security for testing the application.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'allowed_users.txt')
    with open(file_path, "r") as file:
        authorized_users = [line.strip() for line in file]

    if user_email not in authorized_users:
        st.error("You are not authorized to access this page.")
        st.stop()
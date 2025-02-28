import os
import streamlit as st
import stripe
import urllib.parse
from dotenv import load_dotenv
from .utils_auth import get_secret_value

load_dotenv("config.env")

GCP_PROJECT_NUMBER = os.getenv("GCP_PROJECT_NUMBER")


def get_api_key() -> str:
    """
    Retrieves the Stripe API key based on the current mode (testing or production).
    When mode is testing, the key is fetched from the secrets. Otherwise, it is fetched from the GCP Secret Manager.
    
    Returns:
        str: The Stripe API key.
    Raises:
        Exception: If there is an error while fetching the Stripe key from the Secret Manager in production mode.
    """
    testing_mode = st.secrets.get("testing_mode", False)
    
    if testing_mode:
        secret_value = st.secrets["stripe_api_key_test"]
    else:
        try:
            secret_value = get_secret_value(GCP_PROJECT_NUMBER, "STRIPE_API_KEY")
        except Exception as e:
            st.error(f"Error while fetching the Stripe API Key: {e}")
    return secret_value

def get_stripe_link() -> str:
    """
    Retrieves the Stripe API link based on the current mode (testing or production).
    When mode is testing, the link is fetched from the secrets. Otherwise, it is fetched from the GCP Secret Manager.
    
    Returns:
        str: The Stripe API link.
    Raises:
        Exception: If there is an error while fetching the Stripe link from the Secret Manager in production mode.
    """
    testing_mode = st.secrets.get("testing_mode", False)
    
    if testing_mode:
        secret_value = st.secrets["stripe_api_link_test"]
    else:
        try:
            secret_value = get_secret_value(GCP_PROJECT_NUMBER, "STRIPE_LINK")
        except Exception as e:
            st.error(f"Error while fetching the Stripe Link from Secret Manager: {e}")
    return secret_value
    

def redirect_button(
    text: str,
    customer_email: str,
    color="#FD504D"
):
    """
    Creates a redirect button in the Streamlit sidebar that links to a Stripe payment page.

    Args:
        text (str): The text to display on the button.
        customer_email (str): The customer's email to prefill in the Stripe payment page.
        color (str, optional): The background color of the button. Defaults to "#FD504D".

    Returns:
        None
    """
    stripe.api_key = get_api_key()
    stripe_link = get_stripe_link()
    encoded_email = urllib.parse.quote(customer_email)
    button_url = f"{stripe_link}?prefilled_email={encoded_email}"

    st.sidebar.markdown(
        f"""
    <a href="{button_url}" target="_blank">
        <div style="
            display: inline-block;
            padding: 0.5em 1em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 3px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """,
        unsafe_allow_html=True,
    )


def is_active_subscriber(email: str) -> bool:
    """
    Checks if the given email belongs to an active subscriber.

    This function uses the Stripe API to check if there is an active subscription
    associated with the provided email address. It retrieves the customer data
    based on the email and then checks for any active subscriptions.

    Args:
        email (str): The email address of the customer to check.

    Returns:
        bool: True if the customer has an active subscription, False otherwise.
    """
    stripe.api_key = get_api_key()
    customers = stripe.Customer.list(email=email)
    try:
        customer = customers.data[0]
    except IndexError:
        return False

    subscriptions = stripe.Subscription.list(customer=customer["id"])
    st.session_state.subscriptions = subscriptions

    return len(subscriptions) > 0

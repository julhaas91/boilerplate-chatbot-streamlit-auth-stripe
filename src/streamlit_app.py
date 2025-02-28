import os
import streamlit as st
from dotenv import load_dotenv
from authentication_paywall import add_auth
import vertexai
from vertexai.generative_models import GenerativeModel

load_dotenv("config.env")

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")


def create_philosopher_prompt(philosopher: str) -> str:
    """
    Create a prompt for the generative model that instructs it to generate content
    in the style of a given philosopher.

    Args:
        philosopher (str): The name of the philosopher.

    Returns:
        str: The prompt for the generative model.
    """
    return f"""You are now embodying the philosophical perspective and writing style of {philosopher}. 
    You must respond to all questions as {philosopher} would, using their characteristic manner of expression, 
    drawing from their key ideas and philosophical framework, and referencing their major works when relevant. 
    Maintain their unique voice, terminology, and worldview throughout the response. 
    If the question concerns topics or events that came after {philosopher}'s time, 
    analyze them through their philosophical lens and theoretical framework. Answer in Markdown format."""


vertexai.init(project=GCP_PROJECT_ID, location="europe-west3")

philosopher_options = ["Socrates", "Plato", "Aristotle", "Nietzsche", "Kant"]
model_options = ["gemini-1.5-flash", "gemini-1.5-pro"]


def main():
    """
    Main function to run the Streamlit application.
    
    Sets up authentication, sidebar options, and handles the chat interface
    for interacting with a philosopher AI.
    """
    add_auth(
        login_button_text="Login with Google",
        login_button_color="#FD504D",
        login_sidebar=False
    )

    with st.sidebar:
        selected_philosopher = st.selectbox(
            "Choose a philosopher to talk to", 
            philosopher_options
        )
        model_name = "gemini-1.5-flash"

    st.title("💬 Talk to a philosopher")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "philosopher", "content": f"Hello my friend. What do you want to talk about today?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    if prompt := st.chat_input():
        model = GenerativeModel(
            model_name,
            system_instruction=[create_philosopher_prompt(selected_philosopher)]
        )

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = model.generate_content(prompt)
        
        msg = response.text
        
        st.session_state.messages.append({"role": "philosopher", "content": msg})
        st.chat_message("philosopher").write(msg)


if __name__ == "__main__":
    main()

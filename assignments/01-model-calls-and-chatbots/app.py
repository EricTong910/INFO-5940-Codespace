# Streamlit builds the page; OpenAI provides the client for model API calls.
import streamlit as st
from openai import OpenAI

# Use the API key and Cornell gateway address from our environment.
# Creating the client prepares the connection; the model call happens below.
client = OpenAI()
st.title("Our Chatbot")

# After editing this instruction, click New conversation to use it.
system_prompt = "Explain programming concepts using simple analogies and keep each answer under three sentences."

# This returns True on the run triggered by clicking the button.
new_conversation = st.button("New conversation")

# Streamlit reruns this file after each submission or button click.
# Session state keeps our messages between runs. Initialize it or start over.
if "messages" not in st.session_state or new_conversation:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# Redraw earlier messages. Keep the system instruction out of the visible chat.
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Returns submitted text, or None when no message was submitted on this run.
question = st.chat_input("Ask a question")

# Only call the model when the user submits a new message.
if question:
    # Make a new list containing the saved conversation and the new question.
    request_messages = st.session_state.messages + [
        {"role": "user", "content": question}
    ]

    # Show the new question.
    with st.chat_message("user"):
        st.markdown(question)

    # OPTION 1: Wait for the complete answer.
    # Disabled for Experiment 3 because Option 2 streaming is enabled.
    # response = client.chat.completions.create(
    #     model="openai.gpt-4o",
    #     messages=request_messages,
    # )
    # answer = response.choices[0].message.content
    #
    # with st.chat_message("assistant"):
    #     st.markdown(answer)

    # OPTION 2: Stream the answer as it arrives.
    stream = client.chat.completions.create(
        model="openai.gpt-4o",
        messages=request_messages,
        stream=True,
    )

    with st.chat_message("assistant"):
        answer = st.write_stream(stream)

    # Save both sides of this exchange so the next request can include them.
    st.session_state.messages = request_messages + [
        {"role": "assistant", "content": answer}
    ]
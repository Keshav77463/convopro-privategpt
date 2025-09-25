import streamlit as st

from services.get_models_list import get_ollama_models_list
from services.get_title import get_chat_title
from services.chat_utilities import get_answer

from db.conversations import (
    create_new_conversation,
    add_message,
    get_conversation,
    get_all_conversations,
)

# ---------------- UI Setup ----------------
st.set_page_config(page_title="ChatGPT Clone", page_icon="💬", layout="centered")
st.title("💬 Local ChatGPT Clone")

# ---------------- Models ----------------
if "OLLAMA_MODELS" not in st.session_state:
    st.session_state.OLLAMA_MODELS = get_ollama_models_list()

selected_model = st.selectbox("Select Model", st.session_state.OLLAMA_MODELS)

# ---------------- Session State ----------------
st.session_state.setdefault("conversation_id", None)
st.session_state.setdefault("conversation_title", None)
st.session_state.setdefault("chat_history", [])

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("💬 Chat History")

    conversations = get_all_conversations()  # {id: title}

    if st.button("+ New Chat"):
        st.session_state.conversation_id = None
        st.session_state.conversation_title = None
        st.session_state.chat_history = []
        st.rerun()

    for conv_id, title in conversations.items():
        if st.button(title, key=conv_id):
            st.session_state.conversation_id = conv_id

            doc = get_conversation(conv_id)

            if doc:
                st.session_state.chat_history = doc.get("messages", [])
                st.session_state.conversation_title = doc.get("title")

            st.rerun()

# ---------------- Display Chat ----------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- User Input ----------------
user_input = st.chat_input("Type your message...")

if user_input:

    # 🟢 New conversation
    if st.session_state.conversation_id is None:

        title = get_chat_title(selected_model, user_input)

        conv_id = create_new_conversation(
            title=title,
            role="user",
            content=user_input
        )

        st.session_state.conversation_id = conv_id
        st.session_state.conversation_title = title
        st.session_state.chat_history = [
            {"role": "user", "content": user_input}
        ]

    # 🟡 Existing conversation
    else:
        add_message(st.session_state.conversation_id, "user", user_input)

        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

    # 🔵 Get AI response
    response = get_answer(selected_model, st.session_state.chat_history)

    # Save assistant response
    add_message(st.session_state.conversation_id, "assistant", response)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": response}
    )

    st.rerun()
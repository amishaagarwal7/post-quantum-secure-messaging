import streamlit as st
from core.multi_user_system import create_user, send_message
from storage import add_user, get_users, add_message, get_messages

st.set_page_config(page_title="Secure Chat", layout="centered")

st.title("🔐 Post-Quantum Secure Chat")

# ---------------- SESSION STATE ----------------
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ---------------- LOGIN ----------------
if st.session_state.current_user is None:

    st.header("👤 Enter your username")

    username = st.text_input("Username")

    if st.button("Enter Chat"):
        if username.strip() == "":
            st.warning("Username cannot be empty")
        else:
            # Save user globally
            add_user(username)

            # Create crypto identity (in backend)
            create_user(username)

            st.session_state.current_user = username
            st.success(f"Welcome {username}")
            st.rerun()

# ---------------- CHAT UI ----------------
else:
    current_user = st.session_state.current_user

    st.sidebar.header("👤 Logged in as")
    st.sidebar.write(current_user)

    user_list = get_users()
    other_users = [u for u in user_list if u != current_user]

    if len(other_users) == 0:
        st.warning("No other users available. Open another tab and join.")
    else:
        chat_user = st.sidebar.selectbox("💬 Chat with", other_users)

        st.markdown(f"### 💬 Chat with {chat_user}")

        # ---------------- SHOW MESSAGES ----------------
        messages = get_messages()

        for msg in messages:
            if (
                (msg["sender"] == current_user and msg["receiver"] == chat_user)
                or
                (msg["sender"] == chat_user and msg["receiver"] == current_user)
            ):
                if msg["sender"] == current_user:
                    st.markdown(f"🟢 **You:** {msg['text']}")
                else:
                    st.markdown(f"🔵 **{msg['sender']}:** {msg['text']}")

        # ---------------- SEND MESSAGE ----------------
        st.markdown("---")
        message = st.text_input("Type your message")

        if st.button("Send"):
            if message.strip() == "":
                st.warning("Message cannot be empty")
            else:
                result = send_message(current_user, chat_user, message)

                if result:
                    decrypted_text, is_valid = result

                    if is_valid:
                        # Save message globally
                        add_message(current_user, chat_user, decrypted_text)

                        st.success("Message sent securely ✅")
                        st.rerun()
                    else:
                        st.error("Signature verification failed ❌")

        # ---------------- LOGOUT ----------------
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout"):
            st.session_state.current_user = None
            st.rerun()

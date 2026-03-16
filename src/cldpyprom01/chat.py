import streamlit as st
import pandas as pd

from cldpyprom01.ai_agent import run_conversation

st.set_page_config(page_title="Resource Manager", page_icon="🗄️", layout="wide")
st.title("Resource Manager — AI Chat")

# ── Session state ────────────────────────────────────────────────────────────
if "display_messages" not in st.session_state:
    st.session_state.display_messages = []
if "claude_messages" not in st.session_state:
    st.session_state.claude_messages = []

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Attach File")
    uploaded_file = st.file_uploader("Excel or CSV", type=["xlsx", "xls", "csv"])

    df_preview = None
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df_preview = pd.read_csv(uploaded_file)
        else:
            df_preview = pd.read_excel(uploaded_file)
        st.success(f"Loaded {len(df_preview)} rows, {len(df_preview.columns)} columns")
        st.dataframe(df_preview, use_container_width=True)

    st.divider()
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.display_messages = []
        st.session_state.claude_messages = []
        st.rerun()

# ── Chat history ─────────────────────────────────────────────────────────────
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input ───────────────────────────────────────────────────────────────
if prompt := st.chat_input("Type your instruction… e.g. 'Upload resources from the attached file, skip those with missing last name'"):

    # Build the full message Claude will see (prompt + optional file data)
    user_content = prompt
    if df_preview is not None:
        csv_str = df_preview.to_csv(index=False)
        user_content = (
            f"{prompt}\n\n"
            f"Attached data ({len(df_preview)} rows, CSV format):\n"
            f"```\n{csv_str}\n```"
        )

    # Display user message
    st.session_state.display_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Append to Claude message history
    st.session_state.claude_messages.append({"role": "user", "content": user_content})

    # Run AI agent
    with st.chat_message("assistant"):
        with st.spinner("Processing…"):
            try:
                response_text, updated_messages = run_conversation(st.session_state.claude_messages)
                st.markdown(response_text)
                st.session_state.display_messages.append({"role": "assistant", "content": response_text})
                st.session_state.claude_messages = updated_messages
            except Exception as e:
                # Roll back the user message so history stays clean
                st.session_state.claude_messages.pop()
                st.session_state.display_messages.pop()
                st.error(f"Error: {e}")

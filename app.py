import streamlit as st
import agent
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="Bank Account Assistant", layout="centered")

# Title
st.title("🏦 Account Management Assistant")

# Sidebar for login / new account
st.sidebar.header("🔐 User Authentication")

# Conversation state
if "history" not in st.session_state:
    st.session_state.history = []

# Define template
template = """
You are an assistant that manages the bank account of users.  
Rules:
- Authenticate the existing user first (need username + password).
- If credentials are missing, politely ask for both.
- For new account creation:
  * Require username and password
  * All new accounts start with a default balance of 500
  * If any information is missing, politely ask for it
- Authentication is NOT required for new users creating an account.
- If query is irrelevant to bank account, politely refuse.
Query: {task}
"""

# User task
query = st.text_area("💬 Ask me something about your account:")

# Action button
if st.button("Submit Query"):
    if query.strip() == "":
        st.warning("⚠️ Please enter a query.")
    else:
        try:
            prompt = PromptTemplate.from_template(template).format(task=query)
            response = (agent.agent.invoke(prompt))["output"]

            # Save chat history
            st.session_state.history.append(("You", query))
            st.session_state.history.append(("Assistant", response))

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Show chat history
st.subheader("📜 Conversation History")
for role, msg in st.session_state.history:
    if role == "You":
        st.markdown(f"**🧑 {role}:** {msg}")
    else:
        st.markdown(f"**🤖 {role}:** {msg}")

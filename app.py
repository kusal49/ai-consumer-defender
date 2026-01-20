import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

# Import our custom backend logic
from backend import get_legal_agent

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Consumer Rights Defender", page_icon="⚖️")
st.title("⚖️ The Consumer Rights Defender")
st.caption("Powered by **Llama 3** & **Tavily Search**")

# --- SIDEBAR ---
with st.sidebar:
    st.header("About")
    st.markdown("""
    This agent separates **Logic** from **UI**.
    - **Frontend:** Streamlit
    - **Backend:** LangChain + Groq
    - **Tools:** Tavily (Real-time Search)
    """)
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# --- STATE MANAGEMENT ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- MAIN LOGIC ---
def main():
    # Input Area
    user_input = st.text_area("Describe your grievance:", 
        placeholder="E.g., My landlord is refusing to return my security deposit of ₹20,000...",
        height=150
    )

    if st.button("Draft Legal Notice"):
        if not user_input:
            st.warning("Please describe your issue first.")
            return

        # Display a status spinner while the backend works
        with st.spinner("🔍 Agent is searching laws & drafting notice..."):
            try:
                # 1. Initialize the agent from backend
                agent_executor = get_legal_agent()

                # 2. Run the agent
                response = agent_executor.invoke({
                    "input": user_input,
                    "chat_history": st.session_state.chat_history
                })
                
                output_text = response["output"]

                # 3. Display Result
                st.subheader("📜 Drafted Notice")
                st.markdown("---")
                st.markdown(output_text)
                st.markdown("---")
                
                # 4. Save to History
                st.session_state.chat_history.append(HumanMessage(content=user_input))
                st.session_state.chat_history.append(AIMessage(content=output_text))

            except ValueError as e:
                # Catches missing API keys from backend validation
                st.error(f"Configuration Error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# Run the app
if __name__ == "__main__":
    main()
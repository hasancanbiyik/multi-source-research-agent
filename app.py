import os
import streamlit as st
from dotenv import load_dotenv
from main import run_agent_question  # we’ll call into your pipeline

load_dotenv()  # so OPENAI_API_KEY is available

st.set_page_config(
    page_title="Multi-Source Research Agent",
    page_icon="🕵️",
    layout="wide",
)

# Sidebar
st.sidebar.title("Multi-Source Research Agent")
st.sidebar.markdown(
    "This tool collects web results and Reddit discussion, "
    "analyzes them with an LLM, and synthesizes an answer."
)

api_key = os.getenv("OPENAI_API_KEY", "")
if not api_key:
    st.sidebar.error("Missing OPENAI_API_KEY in .env")

st.sidebar.markdown("---")
st.sidebar.caption("Built with LangGraph, DuckDuckGo, Reddit JSON, and OpenAI GPT-4o.")

st.title("Ask a question")
user_query = st.text_input(
    "Example: 'What are people saying about getting an H1B after graduation?'",
    value="",
    placeholder="Ask me anything...",
)

run_clicked = st.button("Run Research")

if run_clicked:
    if not user_query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Collecting sources and analyzing..."):
            try:
                final_state = run_agent_question(user_query)
            except Exception as e:
                st.error(f"Something went wrong while running the agent: {e}")
                final_state = None

        if final_state:
            # Final synthesized answer
            final_answer = final_state.get("final_answer", "")
            st.subheader("Answer")
            if final_answer:
                st.write(final_answer)
            else:
                st.write("No final answer was generated.")

            st.markdown("---")

            # Optional: Show evidence / intermediates
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("### Web Results Summary")
                google_analysis = final_state.get("google_analysis")
                if google_analysis:
                    st.write(google_analysis)
                else:
                    st.write("_No web summary available._")

            with col2:
                st.markdown("### Reddit Summary")
                reddit_analysis = final_state.get("reddit_analysis")
                if reddit_analysis:
                    st.write(reddit_analysis)
                else:
                    st.write("_No reddit summary available._")

            with col3:
                st.markdown("### Bing/Alt Web Summary")
                bing_analysis = final_state.get("bing_analysis")
                if bing_analysis:
                    st.write(bing_analysis)
                else:
                    st.write("_No secondary web summary available._")

            st.markdown("---")

            # Raw links from Reddit
            selected_urls = final_state.get("selected_reddit_urls")
            if selected_urls:
                st.markdown("### Relevant Reddit Threads")
                for url in selected_urls:
                    st.write(f"- {url}")
            else:
                st.markdown("### Relevant Reddit Threads")
                st.write("_No Reddit threads selected._")

            # Raw snippets from web (optional debug mode)
            with st.expander("View raw web results (debug)"):
                st.write(final_state.get("google_results"))

            with st.expander("View fetched Reddit comments (debug)"):
                st.write(final_state.get("reddit_post_data"))

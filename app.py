import streamlit as st
import asyncio

from AI_BLOG_Writter.crew_agentic import build_blog_crew


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Blog Writer",
    page_icon="✍️",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS - Center Content
# --------------------------------------------------
st.markdown(
    """
    <style>

    /* Main content container */
    .block-container {
        max-width: 900px;
        margin: auto;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* Center main title */
    h1 {
        text-align: center;
    }

    /* Center subtitle */
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    /* Center button */
    div.stButton {
        display: flex;
        justify-content: center;
    }

    div.stButton > button {
        width: 220px;
    }

    /* Blog output */
    .blog-container {
        max-width: 850px;
        margin: auto;
        line-height: 1.8;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("✍️ AI Blog Writer")

st.markdown(
    '<p class="subtitle">'
    'Multi-Agent AI system that researches, analyzes, writes, and edits your blog.'
    '</p>',
    unsafe_allow_html=True
)

# -----------------------------
# User Input
# -----------------------------
topic = st.text_input(
    "Enter Blog Topic",
    placeholder="Example: What is Generative AI?"
)


# -----------------------------
# Generate Button
# -----------------------------
if st.button("🚀 Generate Blog", type="primary"):

    if not topic.strip():
        st.warning("Please enter a blog topic.")
        st.stop()

    # Show progress
    with st.spinner("AI agents are working on your blog..."):

        try:
            # Build Crew
            crew = build_blog_crew(topic)

            # Run asynchronous CrewAI execution
            result = asyncio.run(crew.kickoff_async())

            # -----------------------------
            # Display Result
            # -----------------------------
            st.success("Blog generated successfully!")

            st.markdown("---")
            st.subheader("📝 Final Blog")

            # Convert CrewOutput to string
            st.markdown(str(result))

            # -----------------------------
            # Download Button
            # -----------------------------
            st.download_button(
                label="📥 Download Blog",
                data=str(result),
                file_name=f"{topic.replace(' ', '_')}.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error("An error occurred while generating the blog.")
            st.exception(e)
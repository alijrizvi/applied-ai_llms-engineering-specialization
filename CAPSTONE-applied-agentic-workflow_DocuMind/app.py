# DocuMind - Streamlit Dashboard
# The UI Layer for the Project, which Customers will Interact with for Results
# Will Run this with: "streamlit run app.py"

import streamlit as st
import json
import os
import plotly.graph_objects as go
from pipeline import run_pipeline, ingest_mode
from memory import load_memory, clear_memory
from evals import evaluate_report, run_smoke_test
from rag_store import retrieve


# ============================================================
# PAGE CONFIGURATION
# Must be the first Streamlit call in the script
# Sets the Browser tab Title, Icon, and Sidebar default state
# ============================================================

st.set_page_config(
    page_title="DocuMind — AI Knowledge Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# Injects Styling directly into the Streamlit app
# Gives DocuMind a clean, dark-accented professional look without needing a separate CSS file
# ============================================================

st.markdown("""
<style>
    /* Main title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4F8BF9;
        margin-bottom: 0;
    }
    /* Subtitle under the main title */
    .sub-title {
        font-size: 1rem;
        color: #888;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    /* Styling for each report section card */
    .report-section {
        background-color: #1E1E2E;
        border-left: 4px solid #4F8BF9;
        padding: 1rem 1.2rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
    /* Score badge styling used in the eval page */
    .score-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .score-pass { background-color: #1a472a; color: #69db7c; }
    .score-fail { background-color: #4a1010; color: #ff6b6b; }
</style>
""", unsafe_allow_html = True)


# ============================================================
# SIDEBAR NAVIGATION
# Creates the left sidebar with Page links and Project info
# "st.session_state" persists data across Streamlit reruns
# (Streamlit reruns the entire script on every interaction)
# ============================================================

with st.sidebar:
    st.markdown("## **Ali J. Rizvi**")
    st.markdown("""
        <div style="display: flex; gap: 16px; align-items: center; margin-top: 6px; margin-bottom: 6px;">
            <a href="https://github.com/alijrizvi" target="_blank" title="GitHub">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg"
                    width = "44" style="filter: invert(1); opacity: 1.0;"/>
            </a>
            <a href="https://www.linkedin.com/in/ali-jazib-rizvi" target="_blank" title="LinkedIn">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg"
                    width = "44" style="filter: invert(1); opacity: 1.0;"/>
            </a>
            <a href="https://medium.com/@alijrizvi" target="_blank" title="Medium Articles">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/medium.svg"
                    width = "44" style="filter: invert(1); opacity: 1.0;"/>
            </a>
        </div>
    """, unsafe_allow_html = True)
    st.markdown("**Capstone — AI Engineering Specialization**")
    st.markdown("---")
    st.markdown("### 🧠 DocuMind")
    st.markdown("*AI Knowledge Agent Platform*")
    st.divider()

    # Navigation radio — controls which Page renders below
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📄 Upload & Ingest", "💬 Ask DocuMind", "📊 Evaluation", "🧠 Memory"],
        label_visibility = "collapsed"
    )

    st.divider()

    # Project Metadata shown at the bottom of the sidebar
    st.markdown("**Stack**")
    st.markdown("OpenAI · ChromaDB · FastAPI")
    st.markdown("RAG · Multi-Agent · MCP")


# ============================================================
# PAGE 1: HOME
# Landing page with project overview and quick-start guide
# Gives visitors (and recruiters) an instant understanding of what DocuMind does and how it works
# ============================================================

if page == "🏠 Home":
    st.markdown('<p class="main-title">🧠 DocuMind</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">AI Knowledge Agent Platform · RAG · Multi-Agent · MCP · Memory</p>', unsafe_allow_html=True)

    # Three-column feature overview
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📄 **Upload any document**\n\nPDF or TXT files get chunked, embedded with OpenAI, and stored in ChromaDB — a real vector database.")

    with col2:
        st.info("🤖 **Multi-agent pipeline**\n\nPlanner → Worker → Critic (reflection loop) → Writer. Four specialized agents collaborate on every question.")

    with col3:
        st.info("🔌 **MCP tool integration**\n\nAgents can call web search, calculator, and file manager tools mid-workflow — dynamically, based on the question.")

    st.divider()

    # How it works — step by step
    st.markdown("### How it works")
    steps = [
        ("**1️⃣ Upload**", "Go to **Upload & Ingest** and drop in a PDF or TXT file. DocuMind chunks and embeds it into the vector store."),
        ("**2️⃣ Ask**", "Go to **Ask DocuMind** and type any question about your document. The pipeline runs automatically."),
        ("**3️⃣ Review**", "Read the structured report — title, summary, and per-section answers with sources cited."),
        ("**4️⃣ Evaluate**", "Go to **Evaluation** to see groundedness, relevance, and completeness scores for the last report."),
    ]

    for title, desc in steps:
        with st.expander(title):
            st.markdown(desc)

    st.divider()

    # Architecture Diagram as a clean text Overview
    st.markdown("### Architecture")
    st.code("""
        User Question
            │
            ▼
        Planner Agent        ← Decomposes into Subtasks
            │
            ▼
        Worker Agent         ← RAG Retrieval + MCP tools
            │
            ▼
        Critic Agent         ← Scores & Reflects (up to 2 retries)
            │
            ▼
        Writer Agent         ← Synthesizes Final Structured Report
            │
            ▼
        Evaluation Layer     ← Groundedness | Relevance | Completeness
    """, language = "text")


# ============================================================
# PAGE 2: UPLOAD & INGEST
# Lets users Upload a PDF or TXT file directly in the browser
# The file is saved to the uploads/ folder, then passed to "ingest_mode()"" which Chunks + Embeds it into ChromaDB
# ============================================================

elif page == "📄 Upload & Ingest":
    st.markdown("## 📄 Upload & Ingest")
    st.markdown("Upload a PDF or TXT document. DocuMind will chunk, embed, and store it in the vector database — ready for querying.")

    # File Uploader widget — Accepts PDF and TXT only
    uploaded_file = st.file_uploader(
        "Drop your document here",
        type=["pdf", "txt"],
        help="PDF and TXT files supported. Each page (PDF) or 500-char chunk (TXT) becomes one vector."
    )

    if uploaded_file is not None:
        # Show file details before Ingestion
        st.markdown(f"**File:** `{uploaded_file.name}` · **Size:** {round(uploaded_file.size / 1024, 1)} KB")

        if st.button("🚀 Ingest Document", type="primary"):
            # Save the Uploaded file to the "uploads/" folder on disk
            os.makedirs("uploads", exist_ok=True)
            save_path = os.path.join("uploads", uploaded_file.name)

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Run Ingestion with a live Progress Spinner
            with st.spinner(f"Ingesting {uploaded_file.name}... this may take a moment."):
                try:
                    ingest_mode(save_path)
                    st.success(f"✅ **{uploaded_file.name}** successfully ingested into the vector store!")
                    st.info("You can now go to **Ask DocuMind** and ask questions about this document.")
                except Exception as e:
                    st.error(f"Ingestion failed: {str(e)}")


# ============================================================
# PAGE 3: ASK DOCUMIND
# The main Chat Interface 
# User types a question, the full multi-agent pipeline runs, and the structured report is displayed in a clean card layout
# "session_state" stores the last Report so it Persists across Streamlit reruns without re-running the Pipeline
# ============================================================

elif page == "💬 Ask DocuMind":
    st.markdown("## 💬 Ask DocuMind")
    st.markdown("---")
    st.markdown("### Hey you! Yes, you.")
    st.markdown("You want an easier and faster way to get info from your documents, don't you? 😉")
    st.markdown("Of course you do! And that's why we're here.")
    st.markdown("**Feel free to ask any Question about your uploaded documents.**")
    st.markdown("The complete multi-agent pipeline will run and return a structured report.")

    # Initialize Session State for Report persistence
    # Without this, the Report disappears on every Streamlit rerun
    if "last_report" not in st.session_state:
        st.session_state.last_report = None
    if "last_question" not in st.session_state:
        st.session_state.last_question = ""

    # Question Input box
    question = st.text_area(
        "Your Question",
        placeholder = "Example: What are the main risks mentioned in this document? Summarize the key findings.",
        height = 100
    )

    # Pipeline Trigger button
    if st.button("🧠 Run DocuMind Pipeline", type="primary"):
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            # Run the full Pipeline with a live Status Indicator
            with st.status("Running multi-agent pipeline...", expanded=True) as status:
                st.write("🗂️ Loading memory...")
                st.write("🧠 Planner decomposing your question...")
                st.write("🔍 Worker retrieving context from vector store...")
                st.write("✅ Critic reviewing drafts...")
                st.write("✍️ Writer synthesizing final report...")

                try:
                    report = run_pipeline(question)
                    st.session_state.last_report = report
                    st.session_state.last_question = question
                    status.update(label="Pipeline complete!", state="complete")
                except Exception as e:
                    status.update(label="Pipeline failed.", state="error")
                    st.error(f"Error: {str(e)}")

    # Display the Report if one exists in Session State
    if st.session_state.last_report:
        report = st.session_state.last_report
        st.divider()

        # Report Header
        st.markdown(f"### 📋 {report['title']}")
        st.markdown(f"**Summary:** {report['summary']}")
        st.divider()

        # One Card per Section (one per Subtask the Planner created)
        st.markdown("### Sections")
        for section in report["sections"]:
            st.markdown(f"""
<div class="report-section">
    <strong>Q: {section['question']}</strong><br><br>
    {section['answer']}
</div>
""", unsafe_allow_html=True)

        # Sources Cited at the Bottom
        if report.get("sources_used"):
            st.markdown("**Sources cited:**")
            for source in report["sources_used"]:
                st.markdown(f"- `{source}`")

        # Download Button — Exports the Report as JSON
        st.download_button(
            label="⬇️ Download Report (JSON)",
            data=json.dumps(report, indent=2),
            file_name="documind_report.json",
            mime="application/json"
        )


# ============================================================
# PAGE 4: EVALUATION
# Runs the Eval Framework on the last saved Report and Displays scores as a Plotly radar chart + metric cards
# This is the "proof it works" page for this Portfolio.
# ============================================================

elif page == "📊 Evaluation":
    st.markdown("## 📊 Evaluation")
    st.markdown("Scores the last report on groundedness, relevance, and completeness using an LLM judge.")

    report_path = "outputs/latest_report.json"

    if not os.path.exists(report_path):
        st.warning("No report found yet. Ask a question first on the **Ask DocuMind** page.")
    else:
        # Show the Question Input for Context Retrieval
        question = st.text_input(
            "What was your original question?",
            help="Used to retrieve the same RAG chunks for fair evaluation."
        )

        if st.button("🔍 Run Evaluation", type="primary"):
            if not question.strip():
                st.warning("Please enter your original question.")
            else:
                with st.spinner("Running evaluation..."):
                    try:
                        chunks = retrieve(question)
                        results = evaluate_report(report_path, chunks)

                        if "error" not in results:
                            st.divider()

                            # Top-level Aggregate Metrics in Three columns
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Aggregate Score", f"{results['aggregate_score']:.2f} / 1.00")
                            col2.metric("Sections Passed", f"{results['sections_passed']} / {results['total_sections']}")
                            col3.metric("Verdict", "✅ PASS" if results['verdict'] == 'pass' else "❌ FAIL")

                            st.divider()

                            # Plotly Radar Chart — one spoke per Metric per Section
                            # Visually shows the balance between the three Eval dimensions
                            st.markdown("### Score breakdown")

                            section_scores = results["section_scores"]
                            categories = ["Groundedness", "Relevance", "Completeness"]

                            fig = go.Figure()

                            for i, score in enumerate(section_scores):
                                fig.add_trace(go.Scatterpolar(
                                    r=[
                                        score["groundedness"],
                                        score["relevance"],
                                        score["completeness"],
                                        score["groundedness"]  # close the polygon
                                    ],
                                    theta=categories + [categories[0]],
                                    fill="toself",
                                    name=f"Section {i+1}",
                                    opacity=0.7
                                ))

                            fig.update_layout(
                                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                                showlegend=True,
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                font=dict(color="white")
                            )

                            st.plotly_chart(fig, use_container_width=True)

                            # Per-section Score Cards
                            st.markdown("### Per-section scores")
                            for i, score in enumerate(section_scores):
                                verdict_class = "score-pass" if score["verdict"] == "pass" else "score-fail"
                                verdict_label = "PASS" if score["verdict"] == "pass" else "FAIL"
                                st.markdown(f"""
                                <div class="report-section">
                                    <strong>Section {i+1}</strong> &nbsp;
                                    <span class="score-badge {verdict_class}">{verdict_label}</span><br><br>
                                    Groundedness: <strong>{score['groundedness']:.2f}</strong> &nbsp;|&nbsp;
                                    Relevance: <strong>{score['relevance']:.2f}</strong> &nbsp;|&nbsp;
                                    Completeness: <strong>{score['completeness']:.2f}</strong><br><br>
                                    <em>{score['notes']}</em>
                                </div>
                                """, unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Evaluation failed: {str(e)}")

        # Smoke Test option — Sanity check without a Real Report
        st.divider()
        st.markdown("### Quick smoke test")
        st.markdown("Runs a sanity check on the eval system using dummy data — no document needed.")
        if st.button("⚡ Run Smoke Test"):
            with st.spinner("Running smoke test..."):
                result = run_smoke_test()
                st.success(f"Smoke test score: **{result['overall']:.2f}** — {result['verdict'].upper()}")
                st.info(f"Notes: {result['notes']}")


# ============================================================
# PAGE 5: MEMORY
# Shows the full conversation history stored in "session_memory.json" and lets the User clear it to start a Fresh Session
# ============================================================

elif page == "🧠 Memory":
    st.markdown("## 🧠 Session Memory")
    st.markdown("DocuMind remembers your previous questions and answers within a session. This is the full conversation history.")

    history = load_memory()

    if not history:
        st.info("No memory yet. Ask a question on the **Ask DocuMind** page to start building history.")
    else:
        st.markdown(f"**{len(history)} turns in memory**")
        st.divider()

        # Display each Memory turn as a clean Chat-style card
        for turn in history:
            role = turn["role"]
            content = turn["content"]
            timestamp = turn.get("timestamp", "")[:19]  # Trim to "YYYY-MM-DD HH:MM:SS"

            # Color-code by Role — Blue for User, Green for Assistant
            if role == "user":
                st.markdown(f"""
            <div class="report-section" style="border-left-color: #4F8BF9;">
                <small style="color:#888;">👤 USER · {timestamp}</small><br><br>
                {content}
            </div>
            """, unsafe_allow_html=True)
            else:
                            st.markdown(f"""
            <div class="report-section" style="border-left-color: #69db7c;">
                <small style="color:#888;">🤖 ASSISTANT · {timestamp}</small><br><br>
                {content}
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Clear Memory button with a Confirmation Step
    if st.button("🗑️ Clear All Memory", type = "secondary"):
        clear_memory()
        st.success("Memory cleared. Starting fresh next session.")
        st.rerun()
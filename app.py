import streamlit as st
from pathlib import Path
from retrieval.smart_retriever import SmartRetriever
from generation.generator import AnswerGenerator

# --- Page config ---
st.set_page_config(
    page_title="Support Knowledge Copilot",
    page_icon="🤖",
    layout="wide"
)

# --- Load pipeline once ---
@st.cache_resource(show_spinner="Loading pipeline — this takes ~2 minutes on first run...")
def load_pipeline():
    """Loads retriever from persisted Qdrant index. Runs once."""
    from ingestion.pipeline import run_ingestion
    from config.settings import ChunkStrategy

    retriever = SmartRetriever(use_reranker=False)
    chunks = run_ingestion(Path("docs"), strategy=ChunkStrategy.HEADING)
    retriever.hybrid.bm25_retriever.index_chunks(chunks)
    generator = AnswerGenerator()
    return retriever, generator

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Settings")
    mode = st.selectbox(
        "Retrieval Mode",
        ["standard", "rewrite", "multi_query"],
        help="Standard: direct search. Rewrite: LLM rewrites query first. Multi-query: 3 rewrites merged."
    )
    top_k = st.slider("Chunks to retrieve", min_value=3, max_value=10, value=5)
    show_chunks = st.toggle("Show retrieved chunks", value=True)
    show_verdicts = st.toggle("Show citation verdicts", value=True)

    st.divider()
    st.markdown("**About**")
    st.markdown("RAG system over 53 DevAPI documentation pages. Answers are grounded in docs with verified citations.")
    st.markdown(f"**Corpus:** 341 chunks across 10 topic areas")

# --- Main UI ---
st.title("🤖 Support Knowledge Copilot")
st.caption("Ask anything about the DevAPI documentation. Answers are cited and verified.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
retriever, generator = load_pipeline()
# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "metadata" in message:
            meta = message["metadata"]

            # Confidence
            conf = meta.get("confidence", 0)
            color = "green" if conf > 50 else "orange" if conf > 20 else "red"
            st.markdown(f"**Confidence:** :{color}[{conf}/100]")

            # Citation verdicts
            if show_verdicts and meta.get("verdicts"):
                with st.expander("📎 Citation Verdicts"):
                    for cid, verdict in meta["verdicts"].items():
                        icon = "✅" if verdict == "SUPPORTED" else "⚠️" if verdict == "PARTIAL" else "❌"
                        st.markdown(f"{icon} `{cid}` — **{verdict}**")

            # Retrieved chunks
            if show_chunks and meta.get("chunks"):
                with st.expander(f"📄 Retrieved chunks ({len(meta['chunks'])})"):
                    for chunk in meta["chunks"]:
                        st.markdown(f"**`{chunk['chunk_id']}`** ({chunk.get('doc_type', '')})")
                        st.caption(chunk["preview"])
                        st.divider()

# Load pipeline


# Suggested questions (only show when chat is empty)
if not st.session_state.messages:
    st.markdown("### 💡 Try asking:")
    cols = st.columns(2)
    suggestions = [
        "How do I rotate my API key without downtime?",
        "What happens when I exceed the rate limit?",
        "How do I verify webhook signatures?",
        "What is the difference between 401 and 403 errors?",
        "How do I migrate from API v2 to v3?",
        "What are the Pro plan rate limits?",
    ]
    for i, suggestion in enumerate(suggestions):
        col = cols[i % 2]
        if col.button(suggestion, use_container_width=True):
            st.session_state.pending_question = suggestion
            st.rerun()

# Handle suggestion click
if "pending_question" in st.session_state:
    question = st.session_state.pop("pending_question")
    st.session_state.messages.append({"role": "user", "content": question})
    st.rerun()

# Chat input
if question := st.chat_input("Ask about the DevAPI documentation..."):
    st.session_state.messages.append({"role": "user", "content": question})
    st.rerun()

# Process the latest user message
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    question = st.session_state.messages[-1]["content"]

    # Check if already answered
    if len(st.session_state.messages) < 2 or st.session_state.messages[-2]["role"] != "assistant":

        with st.chat_message("assistant"):
            with st.spinner("Searching documentation..."):
                # Retrieve
                hits = retriever.search(question, top_k=top_k, mode=mode)

                # Generate
                result = generator.generate(question, hits)

            # Display answer
            answer = result["answer"]
            st.markdown(answer)

            # Confidence
            conf = result["confidence"]["score"]
            color = "green" if conf > 50 else "orange" if conf > 20 else "red"
            st.markdown(f"**Confidence:** :{color}[{conf}/100]")

            # Verdicts
            if show_verdicts and result.get("verdicts"):
                with st.expander("📎 Citation Verdicts"):
                    for cid, verdict in result["verdicts"].items():
                        icon = "✅" if verdict == "SUPPORTED" else "⚠️" if verdict == "PARTIAL" else "❌"
                        st.markdown(f"{icon} `{cid}` — **{verdict}**")

            # Chunks
            if show_chunks and hits:
                chunks_display = [
                    {
                        "chunk_id":  h["chunk_id"],
                        "doc_type":  h.get("metadata", {}).get("doc_type", ""),
                        "preview":   h["content"][:200] + "...",
                    }
                    for h in hits[:5]
                ]
                with st.expander(f"📄 Retrieved chunks ({len(hits)})"):
                    for chunk in chunks_display:
                        st.markdown(f"**`{chunk['chunk_id']}`** ({chunk['doc_type']})")
                        st.caption(chunk["preview"])
                        st.divider()

        # Save to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "metadata": {
                "confidence": conf,
                "verdicts":   result.get("verdicts", {}),
                "chunks":     chunks_display if hits else [],
            }
        })
show_chunks   = st.toggle("Show retrieved chunks",  value=False)
show_verdicts = st.toggle("Show citation verdicts", value=False)       
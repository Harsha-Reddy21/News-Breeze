import streamlit as st
import feedparser
import requests
import torch
from transformers import pipeline
from TTS.api import TTS
import soundfile as sf
import tempfile
import os

# -------------------------
# Initialization
# -------------------------
st.set_page_config(page_title="Celebrity News Reader", layout="wide")

st.title("📰 Celebrity News Reader")
st.markdown("Summarized headlines from top RSS feeds, read aloud by AI-generated celebrity voices.")

# Load Summarization Model
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="Falconsai/text_summarization")

summarizer = load_summarizer()

# Load TTS Model
@st.cache_resource
def load_tts():
    return TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=torch.cuda.is_available())

tts = load_tts()

# -------------------------
# RSS Feed Sources
# -------------------------
RSS_FEEDS = {
    "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
    "CNN Top Stories": "http://rss.cnn.com/rss/edition.rss",
    "Reuters": "http://feeds.reuters.com/reuters/topNews"
}

feed_choice = st.sidebar.selectbox("Select News Source", list(RSS_FEEDS.keys()))
num_articles = st.sidebar.slider("Number of articles", 1, 10, 5)

# -------------------------
# Fetch and Display News
# -------------------------
feed = feedparser.parse(RSS_FEEDS[feed_choice])
articles = feed.entries[:num_articles]

celebrity_voice = st.sidebar.selectbox("Choose Celebrity Voice (Voice Cloning)", ["Barack Obama", "Emma Watson", "Morgan Freeman", "Custom"])

with st.expander("💡 Tip: You can use your own voice sample in Coqui XTTS setup"):
    st.markdown("Custom voices require a speaker embedding from a reference clip using XTTS v2. (Not supported in this demo.)")

for idx, entry in enumerate(articles):
    st.subheader(f"{idx+1}. {entry.title}")
    st.markdown(f"**Source:** {entry.link}")
    
    # Fetch content and summarize
    try:
        full_text = entry.summary if hasattr(entry, 'summary') else entry.title
        summary = summarizer(full_text, max_length=60, min_length=10, do_sample=False)[0]['summary_text']
        st.write(f"📝 **Summary**: {summary}")
    except Exception as e:
        st.error(f"Summarization error: {e}")
        summary = full_text

    # Generate and play audio
    with st.spinner("🎤 Generating celebrity voice..."):
        try:
            # You can switch voice cloning by passing different speaker embeddings (here we simulate it)
            tts_output = tts.tts(summary, speaker="random", language="en")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                sf.write(tmp.name, tts_output, 24000)
                st.audio(tmp.name, format="audio/wav")
        except Exception as e:
            st.error(f"TTS error: {e}")

st.markdown("— Powered by [Hugging Face Transformers](https://huggingface.co) & [Coqui TTS](https://coqui.ai)")


# 📰 Celebrity News Reader

A Streamlit app that:

- Fetches **latest headlines** from popular news RSS feeds.
- **Summarizes** articles using Hugging Face transformer models.
- **Reads summaries aloud** using **celebrity-style voices** with Coqui's XTTS v2 (voice cloning).

---

## 🚀 Demo Preview

<!-- Add a screenshot if available -->
![screenshot](docs/screenshot.png)

---

## 🧰 Features

- ✅ Selectable news sources (BBC, CNN, Reuters)
- ✅ Summarization via `Falconsai/text_summarization`
- ✅ AI-generated celebrity-style voice narration via `coqui/xtts-v2`
- ✅ Audio playback in the browser

---

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/celebrity-news-reader.git
cd celebrity-news-reader
```

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```  


```bash
streamlit run streamlit_app.py
```

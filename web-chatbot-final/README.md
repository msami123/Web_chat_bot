# 💬 Web Chat Bot

Simple intelligent chatbot powered by GPT-4 and RAG system.

---

## 🚀 Quick Start

### Step 1: Get OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign in (or create account)
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-proj-...`)

### Step 2: Add API Key

Edit `.env` file and replace `your-api-key-here` with your actual key:

```bash
nano .env
```

Change to:
```
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

Save and close.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run

```bash
streamlit run app.py
```

Opens at: `http://localhost:8501`

---

## ⚠️ Important

**You MUST add your own API key before running!**

The `.env` file has a placeholder. Replace it with your real key from OpenAI.

---

## 📁 Files

- `app.py` - Main application
- `knowledge_webbot.json` - Knowledge base
- `system_prompt_webbot.json` - System instructions
- `requirements.txt` - Python dependencies
- `.env` - **Add your API key here!**

---

## ✨ Features

✅ Bilingual (Arabic/English)
✅ Auto language detection
✅ ChatGPT-like interface
✅ 4 quick action buttons
✅ RAG-based responses

---

## 🆘 Troubleshooting

**Error: 401 Invalid API Key**
→ Update `.env` with your actual OpenAI API key

**Error: File not found**
→ Make sure all files are in the same directory

**Error: Module not found**
→ Run `pip install -r requirements.txt`

---

## 📖 Full Instructions

See `FIX_API_KEY_ERROR.md` for detailed API key setup guide.

---

**Need API key?** Get free $5 credit at: https://platform.openai.com/api-keys

**Ready to chat!** 🎉

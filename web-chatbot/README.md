# 💬 Web Chat Bot

Simple intelligent chatbot powered by GPT-4 and RAG system.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run
```bash
streamlit run app.py
```

### 3. Open Browser
The app will open at: `http://localhost:8501`

---

## 📁 Files

- `app.py` - Main application
- `knowledge_webbot.json` - Knowledge base
- `system_prompt_webbot.json` - System instructions
- `requirements.txt` - Python dependencies
- `.env` - API key (already configured)

---

## ⚙️ Configuration

The `.env` file contains your OpenAI API key. It's already set up and ready to use.

---

## ✨ Features

✅ Bilingual (Arabic/English)
✅ Auto language detection
✅ ChatGPT-like interface
✅ 4 quick action buttons
✅ RAG-based responses

---

## 🔒 Security Note

⚠️ **IMPORTANT**: Change the API key in `.env` file before deploying to production.

Get a new key at: https://platform.openai.com/api-keys

---

## 🆘 Troubleshooting

**Problem**: API key error
**Solution**: Check `.env` file exists and contains valid key

**Problem**: File not found errors
**Solution**: Make sure all files are in the same directory

---

## 📞 Need Help?

Check the `.env` file:
```bash
cat .env
```

Should show:
```
OPENAI_API_KEY=sk-proj-...
```

---

**Ready to use!** 🎉

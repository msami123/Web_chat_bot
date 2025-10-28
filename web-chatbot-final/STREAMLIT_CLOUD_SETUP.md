# 🚀 Streamlit Cloud Setup - Complete Guide

## ✅ You're on Streamlit Cloud!

The error means you need to add your API key to **Streamlit Secrets**.

---

## 📝 Step-by-Step Solution:

### Step 1: Get Your API Key

1. Go to: **https://platform.openai.com/api-keys**
2. Sign in (or create free account)
3. Click **"Create new secret key"**
4. **Copy the key** (starts with `sk-proj-...`)

---

### Step 2: Add to Streamlit Secrets

1. **Click "Manage app"** (bottom right corner of your app)
2. Go to **"Settings"** tab
3. Click **"Secrets"** section
4. Paste this (replace with your actual key):

```toml
OPENAI_API_KEY = "sk-proj-your-actual-key-here"
```

5. Click **"Save"**

---

### Step 3: Restart App

The app will automatically restart after saving secrets.

**✅ Should work now!**

---

## 📸 Visual Guide:

### Location of "Manage app" button:
```
┌─────────────────────────────────────┐
│  Your App                           │
│  ────────────────────────────       │
│                                     │
│  (chat interface)                   │
│                                     │
│                                     │
└─────────────────────────────────────┘
              ▲
    [Manage app] ← Click here (bottom right)
```

### In Settings → Secrets:
```toml
# Paste exactly like this:
OPENAI_API_KEY = "sk-proj-abc123xyz..."

# ⚠️ Important:
# - Use quotes around the key
# - No spaces before/after the =
# - One key per line
```

---

## 🔐 Security Notes:

✅ **Good**: Secrets are encrypted and secure
✅ **Good**: Not visible in public repos
✅ **Good**: Only you can see them

❌ **Never**: Put API keys in code
❌ **Never**: Commit `.env` to GitHub
❌ **Never**: Share your API key publicly

---

## 💰 Free Tier:

OpenAI gives **$5 free credits** when you sign up.

Check usage: https://platform.openai.com/account/usage

---

## 🆘 Still Not Working?

### Check 1: Correct Format
Make sure your secrets file looks exactly like:
```toml
OPENAI_API_KEY = "sk-proj-..."
```

### Check 2: Valid Key
- Must start with `sk-proj-`
- Copy the entire key
- No extra spaces

### Check 3: App Restarted
- After saving secrets, app restarts automatically
- Wait 10-20 seconds
- Refresh the page

---

## 🎯 Common Mistakes:

❌ **Wrong:**
```toml
OPENAI_API_KEY=sk-proj-...         # Missing quotes
OPENAI_API_KEY = sk-proj-...       # Missing quotes
OPENAI_API_KEY="sk-proj-..."       # No space after =
```

✅ **Correct:**
```toml
OPENAI_API_KEY = "sk-proj-..."
```

---

## 📋 Complete Checklist:

- [ ] Got API key from OpenAI
- [ ] Clicked "Manage app"
- [ ] Opened "Settings" → "Secrets"
- [ ] Added key in correct format
- [ ] Saved and waited for restart
- [ ] Refreshed the page

---

**After this, your chatbot will work perfectly on Streamlit Cloud!** 🎉

Need API key? → https://platform.openai.com/api-keys

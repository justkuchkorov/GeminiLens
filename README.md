# 🔍 Gemini Lens

**Gemini Lens** is a lightweight, AI-powered "Heads-Up Display" for your desktop. It allows you to highlight any text in any application (Telegram, Browser, PDFs, etc.) and instantly get a professional breakdown using the **Gemini 2.5 Flash** model.

> **Note:** This is my first project fully architected and implemented by an AI agent (Gemini CLI) while collaborating with me!

---

## 🚀 Features
- **OS-Level Hotkey:** Press `Ctrl + Shift + Space` anywhere to trigger.
- **Modular UI:** Clean, modern "Modular Card" design with dark mode.
- **Smart Parsing:** Automatically breaks down concepts into "What is it?", "Purpose", "Example", and "Key Insight".
- **Zero Friction:** Reads directly from your clipboard and displays an always-on-top overlay.

## 🛠️ Installation
1. **Clone the Repo:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/GeminiLens.git
   cd GeminiLens
   ```
2. **Install Dependencies:**
   ```bash
   pip install google-genai keyboard pyperclip customtkinter pyautogui python-dotenv
   ```
3. **Setup API Key:**
   Create a `.env` file in the root folder and add:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
4. **Run it:**
   ```bash
   python gemini_lens.py
   ```

## ⌨️ How to Use
1. Highlight any term you don't understand.
2. Press `Ctrl + Shift + Space`.
3. Read the insight and press `ESC` to close.

---
*Created with the help of Gemini CLI Agent.*

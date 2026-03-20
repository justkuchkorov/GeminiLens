import os
import time
import threading
import keyboard
import pyperclip
import pyautogui
import customtkinter as ctk
from google import genai
from dotenv import load_dotenv
import re

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
HOTKEY = "ctrl+shift+space"

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# --- UI DESIGN SETTINGS ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GeminiPopup(ctk.CTk):
    def __init__(self, text_to_research):
        super().__init__()
        
        self.width = 600
        self.height = 550
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        # Outer Frame
        self.bg_frame = ctk.CTkFrame(self, corner_radius=20, border_width=2, border_color="#1F538D", fg_color="#0F0F0F")
        self.bg_frame.pack(fill="both", expand=True)

        # Title/Header
        self.header = ctk.CTkLabel(self.bg_frame, text="LENS AI • INSIGHT", font=("Inter", 12, "bold"), text_color="#5DADE2")
        self.header.pack(pady=(20, 5))

        # The term being researched
        display_term = text_to_research[:50] + "..." if len(text_to_research) > 50 else text_to_research
        self.title_label = ctk.CTkLabel(self.bg_frame, text=display_term.upper(), font=("Inter", 22, "bold"), text_color="white")
        self.title_label.pack(pady=(0, 20), padx=30)

        # Scrollable area
        self.scroll_frame = ctk.CTkScrollableFrame(self.bg_frame, fg_color="transparent", width=540, height=380)
        self.scroll_frame.pack(padx=20, pady=(0, 10), fill="both", expand=True)

        self.loading_label = ctk.CTkLabel(self.scroll_frame, text="Synthesizing knowledge...", font=("Inter", 14, "italic"), text_color="#777")
        self.loading_label.pack(pady=100)

        self.footer = ctk.CTkLabel(self.bg_frame, text="ESC TO DISMISS", font=("Inter", 10, "bold"), text_color="#444")
        self.footer.pack(side="bottom", pady=15)

        self.bind("<Escape>", lambda e: self.destroy())
        self.focus_force()

        threading.Thread(target=self.get_ai_response, args=(text_to_research,), daemon=True).start()

    def add_section(self, icon, title, content):
        if not content or len(content.strip()) < 5: return
        
        card = ctk.CTkFrame(self.scroll_frame, fg_color="#1A1A1A", corner_radius=10)
        card.pack(fill="x", pady=8, padx=5)

        header_text = f"{icon} {title}"
        header = ctk.CTkLabel(card, text=header_text, font=("Inter", 13, "bold"), text_color="#5DADE2", anchor="w")
        header.pack(fill="x", padx=15, pady=(10, 2))

        clean_content = re.sub(r'\*\*|---|#', '', content).strip()
        body = ctk.CTkLabel(card, text=clean_content, font=("Inter", 14), text_color="#D5D8DC", wraplength=500, justify="left", anchor="w")
        body.pack(fill="x", padx=15, pady=(0, 12))

    def get_ai_response(self, text):
        prompt = f"""
        Explain '{text}' in 4 parts. 
        Start each part with these specific labels:
        PART1: WHAT IS IT?
        PART2: WHY IT MATTERS
        PART3: EXAMPLE
        PART4: KEY INSIGHT
        """
        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
            print(f"DEBUG: Received response for {text}")
            self.parse_and_display(response.text)
        except Exception as e:
            print(f"DEBUG ERROR: {e}")
            self.after(0, lambda: self.loading_label.configure(text=f"ERROR: {str(e)}"))

    def parse_and_display(self, text):
        self.loading_label.destroy()
        
        # Try to split by parts
        parts = re.split(r'PART\d:', text)
        
        if len(parts) > 4:
            # We found our parts!
            self.after(0, lambda: self.add_section("💡", "WHAT IS IT?", parts[1]))
            self.after(0, lambda: self.add_section("🎯", "WHY IT MATTERS?", parts[2]))
            self.after(0, lambda: self.add_section("🚀", "REAL WORLD USE", parts[3]))
            self.after(0, lambda: self.add_section("📌", "KEY INSIGHT", parts[4]))
        else:
            # Fallback: Just show the whole thing in one card
            print("DEBUG: Fallback parsing used.")
            self.after(0, lambda: self.add_section("🧠", "AI ANALYSIS", text))

def grab_and_search():
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2) # Longer wait for slow clipboards
    selected_text = pyperclip.paste().strip()
    
    if selected_text:
        print(f"DEBUG: Triggered for '{selected_text[:20]}'")
        # Run UI in main thread
        app = GeminiPopup(selected_text)
        app.mainloop()

if __name__ == "__main__":
    print(f"Gemini Lens Active. Hotkey: {HOTKEY}")
    keyboard.add_hotkey(HOTKEY, grab_and_search)
    keyboard.wait()

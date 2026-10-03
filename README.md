# YB-Sync: Automated YouTube Video Uploader 🚀

YB-Sync ek lightweight aur powerful Python-based automation tool hai jo YouTube videos ko high quality mein download karke seedha aapke YouTube channel par automatic upload kar deta hai—wo bhi bina kisi manual UI prompts ke!

---

## 🌟 Key Features
* **High-Quality Download:** `yt-dlp` ka use karke best video aur audio format fetch karta hai.
* **Smart Metadata Extraction:** Source video ke title, description, aur tags ko automatically extract karke YouTube upload ke waqt use karta hai.
* **OAuth 2.0 Token Caching:** Bar-bar browser login ka jhanjhat khatam! `token.json` ke through secure aur seamless token reuse milta hai.
* **Direct API Integration:** YouTube Data API v3 ka use karke background mein fast uploads handle karta hai.
* **Stealth Cleanup:** Upload poora hone ke baad local temporary files (`.tmp_store/`) ko automatically wipe kar deta hai taaki storage clean rahe.

---

## 🛠️ Tech Stack
* **Language:** Python 3
* **Libraries:** `google-api-python-client`, `google-auth-oauthlib`, `yt-dlp`
* **Version Control:** Git & GitHub (`gh` CLI)

---

## ⚙️ Prerequisites & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/vipinsinghbagri/ytb-atmn.git](https://github.com/vipinsinghbagri/ytb-atmn.git)
   cd yb-sync


## Create and Activate Virtual Environment:

Bash
python3 -m venv venv
source venv/bin/activate
Install Dependencies:

Bash
pip install -r requirements.txt
Add Google Credentials:

Google Cloud Console se apna client_secret.json download karke project root directory mein rakho.

🚀 Usage
Script ko run karne ke liye bas yeh command chalani hai:

Bash
python3 yb.py --url "YOUR_YOUTUBE_VIDEO_URL"
🔒 Security & Privacy
Yeh project sensitive files ko public hone se bachane ke liye strict .gitignore rules follow karta hai:

client_secret.json

token.json

venv/

.tmp_store/

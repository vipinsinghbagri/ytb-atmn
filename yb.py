import os
import sys
import argparse
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import yt_dlp
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# YouTube Data API v3 scope (Video upload ke liye)
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TEMP_DIR = ".tmp_store"

def get_authenticated_service():
    """Google OAuth 2.0 ke through YouTube API client authenticate karega aur token save/reuse karega"""
    creds = None
    
    # Agar pehle se token save hai toh use load kar lo
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        
    # Agar credentials valid nahi hain, toh naya flow chalao
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Naye tokens ko 'token.json' mein save kar do taaki agli baar popup na aaye
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            
    return build("youtube", "v3", credentials=creds)

def download_video(url):
    """yt-dlp use karke highest available quality video aur metadata download karega"""
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": os.path.join(TEMP_DIR, "payload_media.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": False,
    }

    print("[*] Fetching highest quality video and metadata...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        base, _ = os.path.splitext(filename)
        final_filename = base + ".mp4" if os.path.exists(base + ".mp4") else filename
        
        metadata = {
            "title": info_dict.get("title", "Untitled Short"),
            "description": info_dict.get("description", "")[:5000],
            "tags": info_dict.get("tags", [])[:15]
        }
        
    print(f"[+] High-quality download complete: {final_filename}")
    return final_filename, metadata

def upload_to_youtube(youtube, file_path, metadata):
    """YouTube Data API ke through video upload karega"""
    print("[*] Uploading to YouTube...")
    
    body = {
        "snippet": {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata["tags"],
            "categoryId": "24"  # 24 = entertainerment
        },
        "status": {
            "privacyStatus": "public",
           # "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"[~] Upload progress: {int(status.progress() * 100)}%")

    print(f"[+] Upload Successful! Video ID: {response.get('id')}")

def cleanup(file_path):
    """Temporary file ko permanently delete kar dega (Stealth Wipe)"""
    if os.path.exists(file_path):
        os.remove(file_path)
        print("[*] Local cache wiped successfully.")

def main():
    parser = argparse.ArgumentParser(description="YB-Sync CLI Automator")
    parser.add_argument("--url", required=True, help="YouTube Video URL to sync/upload")
    args = parser.parse_args()

    if not os.path.exists("client_secret.json"):
        print("[-] Error: 'client_secret.json' file missing! Google Console se credentials download karke yahan rakho.")
        sys.exit(1)

    try:
        # 1. Authenticate YouTube API
        youtube = get_authenticated_service()

        # 2. Download Media & Extract Metadata
        video_file, metadata = download_video(args.url)

        # 3. Upload to Target Channel
        upload_to_youtube(youtube, video_file, metadata)

    except Exception as e:
        print(f"[-] An error occurred: {e}")

    finally:
        # 4. Cleanup Local Storage
        if 'video_file' in locals():
            cleanup(video_file)

if __name__ == "__main__":
    main()

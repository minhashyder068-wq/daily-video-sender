import os
from pathlib import Path

def upload_video(video_path, title, description, tags, privacy_status="private"):
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.oauth2.credentials import Credentials

    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    token_file = Path(os.getenv("YOUTUBE_TOKEN_FILE", "token.json"))
    client_file = Path(os.getenv("YOUTUBE_CLIENT_SECRETS", "credentials.json"))

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), scopes)
    else:
        if not client_file.exists():
            raise RuntimeError("YouTube OAuth credentials.json is missing.")
        flow = InstalledAppFlow.from_client_secrets_file(str(client_file), scopes)
        creds = flow.run_local_server(port=0)
        token_file.write_text(creds.to_json(), encoding="utf-8")

    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {"title": title, "description": description, "tags": tags, "categoryId": "22"},
        "status": {"privacyStatus": privacy_status}
    }
    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    return response.get("id")

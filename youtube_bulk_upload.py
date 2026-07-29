#!/usr/bin/env python3
"""Bulk upload videos to YouTube in natural filename order."""

from __future__ import annotations

import argparse
import csv
import mimetypes
import os
import re
import sys
import time
from pathlib import Path
from typing import Iterable

SCOPES = ["https://www.googleapis.com/auth/youtube"]
VIDEO_EXTENSIONS = {
    ".3g2",
    ".3gp",
    ".avi",
    ".flv",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpeg",
    ".mpg",
    ".webm",
    ".wmv",
}
RETRIABLE_STATUS_CODES = {500, 502, 503, 504}


def natural_key(path: Path) -> list[object]:
    """Sort names like 1.1, 1.2, 1.10 in numeric order."""
    parts = re.split(r"(\d+)", path.stem.lower())
    return [int(part) if part.isdigit() else part for part in parts]


def iter_video_files(folder: Path) -> list[Path]:
    if not folder.is_dir():
        raise SystemExit(f"Pasta nao encontrada: {folder}")

    videos = [
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS
    ]
    return sorted(videos, key=natural_key)


def get_authenticated_service(client_secrets: Path, token_file: Path):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        if not client_secrets.exists():
            raise SystemExit(
                f"Arquivo OAuth nao encontrado: {client_secrets}\n"
                "Baixe o OAuth Client ID do Google Cloud e salve nesse caminho."
            )
        flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets), SCOPES)
        creds = flow.run_local_server(port=0)
        token_file.write_text(creds.to_json(), encoding="utf-8")

    return build("youtube", "v3", credentials=creds)


def find_playlist_id(youtube, playlist_name: str) -> str:
    page_token = None
    while True:
        response = (
            youtube.playlists()
            .list(
                part="snippet",
                mine=True,
                maxResults=50,
                pageToken=page_token,
            )
            .execute()
        )
        for item in response.get("items", []):
            if item["snippet"]["title"].strip().casefold() == playlist_name.casefold():
                return item["id"]

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    raise SystemExit(f'Playlist "{playlist_name}" nao encontrada no canal autenticado.')


def upload_video(
    youtube,
    video_path: Path,
    title: str,
    description: str,
    category_id: str,
    language: str,
    privacy_status: str,
    max_retries: int,
) -> str:
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category_id,
            "defaultLanguage": language,
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False,
        },
    }

    mime_type = mimetypes.guess_type(video_path.name)[0] or "video/*"
    media = MediaFileUpload(str(video_path), mimetype=mime_type, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    retry = 0
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"  progresso: {int(status.progress() * 100)}%")
        except HttpError as exc:
            if exc.resp.status not in RETRIABLE_STATUS_CODES or retry >= max_retries:
                raise
            retry += 1
            wait_seconds = min(2**retry, 60)
            print(f"  erro temporario {exc.resp.status}; tentando novamente em {wait_seconds}s")
            time.sleep(wait_seconds)
        except OSError:
            if retry >= max_retries:
                raise
            retry += 1
            wait_seconds = min(2**retry, 60)
            print(f"  falha de rede/arquivo; tentando novamente em {wait_seconds}s")
            time.sleep(wait_seconds)

    return response["id"]


def make_video_title(path: Path, max_length: int) -> str:
    max_length = max(1, max_length)
    title = " ".join(path.stem.split())
    if not title:
        title = path.name

    if len(title) <= max_length:
        return title

    shortened = title[:max_length].rstrip(" .-_")
    last_space = shortened.rfind(" ")
    if last_space >= max_length // 2:
        shortened = shortened[:last_space]
    shortened = shortened.rstrip(" .-_")
    return shortened or title[:max_length]


def add_to_playlist(youtube, playlist_id: str, video_id: str) -> None:
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id,
                },
            }
        },
    ).execute()


def write_report_header(path: Path) -> None:
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["arquivo", "video_id", "url", "share_emails"])


def append_report(path: Path, file_name: str, video_id: str, share_emails: Iterable[str]) -> None:
    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                file_name,
                video_id,
                f"https://www.youtube.com/watch?v={video_id}",
                ";".join(share_emails),
            ]
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Faz upload em lote para o YouTube respeitando numeracao dos arquivos."
    )
    parser.add_argument("folder", type=Path, help="Pasta contendo os videos.")
    parser.add_argument("--client-secrets", type=Path, default=Path("client_secrets.json"))
    parser.add_argument("--token-file", type=Path, default=Path("token.json"))
    parser.add_argument("--playlist-id", help="ID da playlist. Se omitido, usa --playlist-name.")
    parser.add_argument("--playlist-name", default="Leilões")
    parser.add_argument("--description", default="")
    parser.add_argument("--category-id", default="22", help="Categoria YouTube. Padrao: 22 (People & Blogs).")
    parser.add_argument("--language", default="pt-BR", help="Idioma dos metadados. Padrao: pt-BR.")
    parser.add_argument("--privacy-status", default="private", choices=["private", "unlisted", "public"])
    parser.add_argument("--title-max-length", type=int, default=100, help="Limite de caracteres do titulo. Padrao: 100.")
    parser.add_argument("--share-email", action="append", default=[], help="Email para registrar no relatorio.")
    parser.add_argument("--report", type=Path, default=Path("youtube_uploads.csv"))
    parser.add_argument("--max-retries", type=int, default=5)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    videos = iter_video_files(args.folder)

    if not videos:
        print(f"Nenhum video encontrado em {args.folder}")
        return 0

    print("Ordem de upload:")
    for index, video in enumerate(videos, start=1):
        print(f"  {index}. {video.name}")

    if args.dry_run:
        return 0

    if args.share_email:
        print(
            "\nAviso: a YouTube Data API nao permite convidar emails para videos privados.\n"
            "O script gravara os emails e links no CSV para convite manual no YouTube Studio.\n"
        )

    youtube = get_authenticated_service(args.client_secrets, args.token_file)
    playlist_id = args.playlist_id or find_playlist_id(youtube, args.playlist_name)
    write_report_header(args.report)

    for video_path in videos:
        print(f"\nEnviando: {video_path.name}")
        title = make_video_title(video_path, args.title_max_length)
        if title != " ".join(video_path.stem.split()):
            print(f"  titulo ajustado para {len(title)} caracteres: {title}")
        video_id = upload_video(
            youtube=youtube,
            video_path=video_path,
            title=title,
            description=args.description,
            category_id=args.category_id,
            language=args.language,
            privacy_status=args.privacy_status,
            max_retries=args.max_retries,
        )
        add_to_playlist(youtube, playlist_id, video_id)
        append_report(args.report, video_path.name, video_id, args.share_email)
        print(f"  ok: https://www.youtube.com/watch?v={video_id}")

    print(f"\nConcluido. Relatorio: {args.report}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuario.", file=sys.stderr)
        raise SystemExit(130)

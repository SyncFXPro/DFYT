import yt_dlp
import os
import uuid
import glob
import re
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import FileResponse, JSONResponse, Response, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
import traceback

app = FastAPI()

# Enable CORS for frontend - allow everything
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Global exception handler to ensure CORS headers on all errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Global exception handler: {type(exc).__name__}: {str(exc)}")
    print(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

# 1. Setup Downloads Directory
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


class DownloadRequest(BaseModel):
    url: str
    type: str



import yt_dlp

def download_logic(url: str, type: str, request_id: str):
    output_dir = os.path.join(DOWNLOAD_DIR, request_id)
    os.makedirs(output_dir, exist_ok=True)
    
    # Use absolute path to ensure yt-dlp knows where to save
    abs_output_dir = os.path.abspath(output_dir)
    outtmpl = os.path.join(abs_output_dir, "%(title)s.%(ext)s")
    
    print(f"Downloading to: {abs_output_dir}")
    print(f"Output template: {outtmpl}")

    ydl_opts = {
        "outtmpl": outtmpl,
        "quiet": False,  # Enable verbose output to see what's happening
    }

    if type.lower() == "video":
        ydl_opts.update({
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "merge_output_format": "mp4",
        })
    elif type.lower() == "audio":
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }],
        })
    else:
        raise ValueError("type must be video or audio")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    files = []
    if os.path.exists(abs_output_dir):
        for item in os.listdir(abs_output_dir):
            item_path = os.path.join(abs_output_dir, item)
            if os.path.isfile(item_path):
                files.append((os.path.getmtime(item_path), item_path, item))
    
    if not files:
        raise RuntimeError(f"No file was downloaded to {abs_output_dir}")
    
    # Get the most recently created file
    files.sort(key=lambda x: x[0], reverse=True)
    filepath = files[0][1]
    filename = os.path.basename(filepath)
    
    return filepath, filename



@app.options("/download/v2")
async def download_v2_options():
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.post("/download/v2")
async def download_v2(request: DownloadRequest):
    request_id = str(uuid.uuid4())
    filepath = None

    try:
        filepath, filename = await run_in_threadpool(
            download_logic,
            request.url,
            request.type,
            request_id
        )

        # Verify file exists before trying to serve it
        if not os.path.exists(filepath):
            raise RuntimeError(f"File at path {filepath} does not exist")
        
        # Read the file and send it as a download response
        with open(filepath, 'rb') as f:
            file_content = f.read()
        
        return Response(
            content=file_content,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Filename": filename,
                "Access-Control-Expose-Headers": "X-Filename, Content-Disposition",
                "Access-Control-Allow-Origin": "*",
            }
        )

    except Exception as e:
        error_detail = str(e)
        print(f"Error in download_v2: {error_detail}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=400,
            content={"detail": error_detail},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            }
        )

    finally:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            output_dir = os.path.dirname(filepath)
            if os.path.exists(output_dir):
                try:
                    os.rmdir(output_dir)
                except OSError:
                    pass  # Directory not empty or other error, ignore


"""
Depricated, use /download/v2 instead.

@app.post("/download")
async def download_endpoint(request: DownloadRequest):
    request_id = str(uuid.uuid4())
    
    try:
        filepath, filename = await run_in_threadpool(
            download_logic, 
            request.url, 
            request.type, 
            request_id
        )
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Filename": filename,
            "Access-Control-Expose-Headers": "Content-Disposition, X-Filename"
        }
        return FileResponse(
            path=filepath, 
            filename=filename, # fallback
            media_type='application/octet-stream',
            headers=headers
        )
    except Exception as e:
        print(f"Server Error: {e}") # Log to server console
        raise HTTPException(status_code=400, detail=str(e))

"""

def download_test():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
        "quiet": False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    #download_test()
    print("Please run from the website, nothing is configured from this file.")
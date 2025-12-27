# Video Downloader

A modern, elegant web application for downloading YouTube videos and audio files. Built with FastAPI backend and vanilla JavaScript frontend, featuring a clean black & white minimalist design.

## Features

- 🎥 **Video Downloads** - Download YouTube videos in MP4 format
- 🎵 **Audio Extraction** - Extract audio as MP3 files
- 🎨 **Modern UI** - Clean, minimalist black & white design
- ⚡ **Fast & Efficient** - Direct file streaming to browser
- 🔄 **Auto-start** - Configure to start automatically on system login
- 🌐 **Network Access** - Accessible from your local network

## Screenshots

The application features a sleek, modern interface with:
- Clean white container on subtle gradient background
- Smooth hover animations and transitions
- Responsive design that works on all devices
- Intuitive user experience

## Requirements

- Python 3.9 or higher
- FFmpeg (for video/audio processing)
- Internet connection

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg:**
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` (Ubuntu/Debian)

## Configuration

The server is configured to run on:
- **IP Address:** `172.22.112.1`
- **Port:** `2847`

To change these settings, edit:
- `launcher.py` - Server IP and port configuration
- `index.js` - Frontend API endpoint URLs

## Usage

### Starting the Server

**Option 1: Using the Launcher (Recommended)**
```bash
python launcher.py
```
or simply double-click `start.bat` on Windows.

**Option 2: Direct uvicorn**
```bash
uvicorn download:app --host 172.22.112.1 --port 2847
```

### Using the Application

1. Start the server using one of the methods above
2. The application will automatically open in your default browser
3. Enter a YouTube URL in the input field
4. Select "Video" or "Audio" from the dropdown
5. Click "Download" to start the download
6. The file will download to your browser's default download location

### Auto-Start on Login

See `STARTUP_PLAN.md` for detailed instructions on setting up automatic startup:
- **Task Scheduler** (Recommended) - Most reliable method
- **Startup Folder** - Simplest method
- **Windows Service** - Advanced method

## Project Structure

```
DFYT/
├── download.py          # FastAPI backend server
├── index.html           # HTML structure
├── index.js             # Frontend JavaScript
├── home.css             # Styling
├── launcher.py          # Server launcher script
├── start.bat            # Windows batch launcher
├── requirements.txt     # Python dependencies
├── STARTUP_PLAN.md      # Auto-startup instructions
└── downloads/            # Temporary download directory
```

## Technical Details

### Backend
- **Framework:** FastAPI
- **Video Processing:** yt-dlp
- **File Handling:** Temporary files cleaned up after serving

### Frontend
- **Vanilla JavaScript** - No frameworks required
- **Modern CSS** - Clean, responsive design
- **Fetch API** - For server communication

### Architecture
1. User enters URL and selects format
2. Frontend sends POST request to `/download/v2`
3. Backend downloads file using yt-dlp
4. File is streamed back to browser with proper headers
5. Browser triggers download with correct filename
6. Temporary files are cleaned up automatically

## API Endpoints

### `POST /download/v2`
Downloads a video or audio file from YouTube.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=...",
  "type": "video"  // or "audio"
}
```

**Response:**
- Returns file as download with `Content-Disposition` header
- Includes `X-Filename` header with the actual filename

### `OPTIONS /download/v2`
CORS preflight handler.

## Troubleshooting

### Server won't start
- Check if Python is installed and in PATH
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check if port 2847 is available (or change it in `launcher.py`)

### Downloads fail
- Ensure FFmpeg is installed and accessible
- Check your internet connection
- Verify the YouTube URL is valid
- Check server console for error messages

### CORS errors
- Ensure the server is running
- Verify IP address matches in both `launcher.py` and `index.js`
- Check browser console for specific error messages

### File format issues
- Video downloads should be MP4 format
- Audio downloads should be MP3 format
- If issues persist, check FFmpeg installation

## Development

### Running in Development Mode
```bash
uvicorn download:app --host 172.22.112.1 --port 2847 --reload
```

### Testing
Test the server by visiting: `http://172.22.112.1:2847/docs` to see the FastAPI documentation.

## Dependencies

See `requirements.txt` for full list:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `yt-dlp` - YouTube downloader
- `pydantic` - Data validation

## License

This project is provided as-is for personal use.

## Contributing

Feel free to fork and modify for your own use. Suggestions and improvements are welcome!

## Notes

- Downloaded files are temporarily stored in the `downloads/` directory
- Files are automatically cleaned up after being served
- The server must be running for the application to work
- Network access allows other devices on your network to use the downloader

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review server console output for errors
3. Check browser console for frontend errors

---

**Enjoy downloading your favorite YouTube content!** 🎉



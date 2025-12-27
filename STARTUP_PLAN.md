# Windows Startup Plan for Video Downloader Server

## Option 1: Task Scheduler (Recommended - Most Reliable)

### Steps:
1. Press `Win + R`, type `taskschd.msc` and press Enter
2. Click "Create Basic Task" in the right panel
3. Name it: "Video Downloader Server"
4. Description: "Auto-start video downloader server on login"
5. Trigger: "When I log on"
6. Action: "Start a program"
7. Program/script: `python`
8. Add arguments: `"H:\DFYT\launcher.py"`
9. Start in: `H:\DFYT`
10. Check "Open the Properties dialog for this task when I click Finish"
11. In Properties:
    - General tab: Check "Run whether user is logged on or not" (optional)
    - General tab: Check "Run with highest privileges" (if needed)
    - Settings tab: Uncheck "Stop the task if it runs longer than" (to keep it running)
    - Settings tab: Check "If the task fails, restart every: 1 minute" (optional)
12. Click OK

### Advantages:
- Runs automatically on login
- Can run in background
- Can restart if it crashes
- Most reliable method

---

## Option 2: Startup Folder (Simplest)

### Steps:
1. Press `Win + R`, type `shell:startup` and press Enter
2. Create a shortcut:
   - Right-click in the folder → New → Shortcut
   - Location: `python H:\DFYT\launcher.py`
   - Name: "Video Downloader Server"
3. Right-click the shortcut → Properties
   - Start in: `H:\DFYT`
   - Run: "Minimized" (optional, to hide window)

### Advantages:
- Very simple
- Easy to disable (just delete shortcut)

### Disadvantages:
- Shows a window (unless minimized)
- Less control over behavior

---

## Option 3: Windows Service (Advanced)

### Steps:
1. Install `nssm` (Non-Sucking Service Manager) from https://nssm.cc/download
2. Open Command Prompt as Administrator
3. Run:
   ```
   nssm install VideoDownloaderServer
   ```
4. In the GUI that opens:
   - Path: `C:\Python39\python.exe` (or your Python path)
   - Startup directory: `H:\DFYT`
   - Arguments: `launcher.py`
5. Go to "Log on" tab and select your user account
6. Click "Install service"
7. Start the service:
   ```
   nssm start VideoDownloaderServer
   ```

### Advantages:
- Runs as a true Windows service
- Can start before user login
- Most professional solution

### Disadvantages:
- More complex setup
- Requires additional software (nssm)

---

## Recommended: Option 1 (Task Scheduler)

Task Scheduler is the best balance of reliability and simplicity. It will:
- Start the server automatically when you log in
- Keep it running in the background
- Optionally restart it if it crashes
- Work even if you're not logged in (if configured)

---

## Testing the Startup

After setting up, test by:
1. Logging out and logging back in
2. Or restarting your computer
3. Check if the server is running by opening: `http://172.22.112.1:2847/docs`
4. If it works, you should see the FastAPI documentation page

---

## Notes

- The server will run on IP: **172.22.112.1** and port: **2847**
- Make sure Python is in your system PATH
- The server will open the HTML file in your browser automatically
- To stop the server, you'll need to end the Python process or use Task Manager


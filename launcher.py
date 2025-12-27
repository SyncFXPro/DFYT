import subprocess
import webbrowser
import time
import os
import sys
import signal
import atexit

# Global variable to store server process
server_process = None

def cleanup():
    """Stop the server when the script exits"""
    global server_process
    if server_process:
        print("\nStopping server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("Server stopped.")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    cleanup()
    sys.exit(0)

def main():
    global server_process
    
    # Register cleanup functions
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Server configuration
    SERVER_PORT = 2847
    SERVER_IP = "172.22.112.1"
    
    print("Starting Video Downloader Server...")
    print(f"Server will be available at http://{SERVER_IP}:{SERVER_PORT}")
    print("Press Ctrl+C to stop the server\n")
    
    # Start the FastAPI server
    try:
        server_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "download:app", "--host", SERVER_IP, "--port", str(SERVER_PORT)],
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Check if server started successfully
        if server_process.poll() is not None:
            print("Error: Server failed to start!")
            return 1
        
        # Get the absolute path to index.html
        script_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(script_dir, "index.html")
        
        # Open the HTML file in the default browser
        print(f"Opening {html_path} in your browser...")
        webbrowser.open(f"file:///{html_path.replace(os.sep, '/')}")
        
        print("\nServer is running. Keep this window open.")
        print("Close this window or press Ctrl+C to stop the server.\n")
        
        # Keep the script running
        try:
            server_process.wait()
        except KeyboardInterrupt:
            pass
        
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}")
        cleanup()
        return 1

if __name__ == "__main__":
    sys.exit(main())


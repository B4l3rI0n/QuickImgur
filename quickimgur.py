import os
import time
import pyperclip
import requests
import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab, Image
from PIL import UnidentifiedImageError
from io import BytesIO
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import signal
import sys

# Configuration
IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID", "your_client_id_here")
UPLOAD_URL = "https://api.imgur.com/3/upload"
WATCH_FOLDER = os.path.expanduser("~/Downloads")
ENABLE_GUI = True  # Enable GUI (paste/select) by default
ENABLE_WATCHER = True  # Enable folder watching by default

# Global flag to signal watcher to stop
watcher_running = True
# Lock for synchronizing console output
print_lock = threading.Lock()

if not os.path.exists(WATCH_FOLDER):
    print(f"Warning: {WATCH_FOLDER} does not exist. File dialog will default to home directory.")

def upload_to_imgur(image_data, is_file=True):
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    files = {"image": image_data} if is_file else {"image": ("clipboard.png", image_data.getvalue(), "image/png")}
    try:
        response = requests.post(UPLOAD_URL, headers=headers, files=files, timeout=10)
        if response.status_code == 200:
            image_url = response.json()["data"]["link"]
            return f"[]({image_url})"
        else:
            return f"Error uploading image: HTTP {response.status_code}"
    except requests.RequestException as e:
        return "Network error: Unable to connect to Imgur. Check your internet connection."

def paste_or_select_and_upload():
    def select_image():
        initial_dir = WATCH_FOLDER if os.path.exists(WATCH_FOLDER) else os.path.expanduser("~")
        try:
            file_path = filedialog.askopenfilename(
                title="Select an Image",
                initialdir=initial_dir,
                filetypes=[
                    ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                    ("All Files", "*.*")
                ]
            )
            if file_path:
                with open(file_path, "rb") as image_file:
                    result = upload_to_imgur(image_file)
                pyperclip.copy(result)
                with print_lock:
                    print(f"Uploaded & copied to clipboard: {result}")
                    print("Returning to menu...")
            else:
                with print_lock:
                    print("No file selected.")
                    print("Returning to menu...")
        except Exception as e:
            with print_lock:
                print(f"Error opening file dialog: {e}")
                print("Returning to menu...")

    def paste_image():
        try:
            image = ImageGrab.grabclipboard()
            if image:
                image_data = BytesIO()
                image.save(image_data, format="PNG")
                result = upload_to_imgur(image_data, is_file=False)
                pyperclip.copy(result)
                with print_lock:
                    print(f"Uploaded & copied to clipboard: {result}")
                    print("Returning to menu...")
            else:
                with print_lock:
                    print("No image found in clipboard! Copy an image (e.g., right-click > Copy Image) and try again.")
                    print("Returning to menu...")
        except UnidentifiedImageError:
            with print_lock:
                print("Invalid image in clipboard! Copy a valid image (e.g., right-click > Copy Image) and try again.")
                print("Returning to menu...")

    root = tk.Tk()
    root.withdraw()
    
    try:
        while True:
            with print_lock:
                sys.stdout.write("Press 'p' to paste, 's' to select, or 'q' to quit: ")
                sys.stdout.flush()
            try:
                choice = input().lower()
            except KeyboardInterrupt:
                with print_lock:
                    print("\nExiting...")
                break
            if choice == 'p':
                paste_image()
            elif choice == 's':
                select_image()
            elif choice == 'q':
                with print_lock:
                    print("Exiting...")
                break
            else:
                with print_lock:
                    print("Please enter 'p', 's', or 'q'.")
                    print("Returning to menu...")
    finally:
        global watcher_running
        watcher_running = False  # Signal watcher to stop
        root.destroy()

class ImageWatcher(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            time.sleep(1)
            with open(event.src_path, "rb") as image_file:
                result = upload_to_imgur(image_file)
            pyperclip.copy(result)
            with print_lock:
                print(f"\nUploaded & copied to clipboard: {result} (from folder watcher)")
                # Reprint GUI prompt if GUI is enabled
                if ENABLE_GUI:
                    sys.stdout.write("Press 'p' to paste, 's' to select, or 'q' to quit: ")
                    sys.stdout.flush()

def watch_folder():
    if not os.path.exists(WATCH_FOLDER):
        with print_lock:
            print(f"Error: {WATCH_FOLDER} does not exist. Cannot start folder watcher.")
        return
    event_handler = ImageWatcher()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    try:
        while watcher_running:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()

def signal_handler(sig, frame):
    global watcher_running
    watcher_running = False
    with print_lock:
        print("\nExiting...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handler for clean exit
    signal.signal(signal.SIGINT, signal_handler)

    # Start folder watcher in a thread if enabled
    watcher_thread = None
    if ENABLE_WATCHER:
        watcher_thread = threading.Thread(target=watch_folder, daemon=True)
        watcher_thread.start()

    # Run GUI if enabled, otherwise keep watcher alive
    if ENABLE_GUI:
        paste_or_select_and_upload()
    elif ENABLE_WATCHER:
        try:
            while watcher_running:
                time.sleep(1)
        except KeyboardInterrupt:
            with print_lock:
                print("\nExiting...")
            watcher_running = False
        if watcher_thread:
            watcher_thread.join()
    else:
        print("No modes enabled. Set ENABLE_GUI or ENABLE_WATCHER to True.")

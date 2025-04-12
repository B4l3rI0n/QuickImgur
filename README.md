# QuickImgur

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

**QuickImgur** is a Python tool to upload images to [Imgur](https://imgur.com) and copy Markdown links (`![](<url>)`) to the clipboard. It supports pasting images from the clipboard, selecting files from your Downloads folder, or automatically uploading new images saved to Downloads. Perfect for bloggers, developers, or anyone needing quick image links for Markdown-based platforms like GitHub or Jekyll blogs.

## Features

- **Clipboard Paste**: Upload images copied to the clipboard (e.g., right-click > Copy Image).
- **File Selection**: Choose images via a GUI file dialog from your Downloads folder.
- **Folder Monitoring**: Automatically upload new images saved to `~/Downloads` or configured directory.
- **Dual Mode**: Run GUI and folder watcher simultaneously for seamless workflow.
- **Markdown Output**: Copies `![](<imgur_url>)` to the clipboard for easy pasting into blogs or READMEs.
- **Error Handling**: Manages network issues, invalid clipboard content, and missing folders.
- **Configurable**: Enable/disable GUI or watcher modes via simple flags.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/QuickImgur.git
   cd QuickImgur

2. **Install Dependencies**:
   Ensure Python 3.6+ is installed, then:
   ```bash
   pip install -r requirements.txt
   ```
   On Linux, you may need Tkinter:
   ```bash
   sudo apt-get install python3-tk
   ```

3. **Get an Imgur Client ID**:
   - Register at [Imgur API](https://api.imgur.com/oauth2/addclient).
   - Copy your Client ID.
   - Set it in `quickimgur.py`:
     ```python
     IMGUR_CLIENT_ID = "your_client_id_here"
     ```
     Alternatively, use an environment variable:
     ```bash
     export IMGUR_CLIENT_ID="your_client_id_here"
     ```
     Then modify `quickimgur.py`:
     ```python
     IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID", "default_client_id")
     ```

## Usage

Run the script:
```bash
python quickimgur.py
```

### GUI Mode
- Prompt: `Press 'p' to paste, 's' to select, or 'q' to quit:`
- **Paste ('p')**: Uploads an image from the clipboard.
- **Select ('s')**: Opens a file dialog to choose an image from `~/Downloads` or home directory.
- **Quit ('q')**: Exits the script, stopping any folder monitoring.
- Output: Copies `![](<imgur_url>)` to the clipboard and prints results.

### Folder Watcher Mode
- Monitors `~/Downloads` for new `.png`, `.jpg`, `.jpeg`, or `.gif` files.
- Automatically uploads new images and copies Markdown links.
- Runs in the background if `ENABLE_WATCHER = True`.

### Configuration
Edit `quickimgur.py` to toggle modes:
```python
ENABLE_GUI = True     # Enable/disable GUI prompt
ENABLE_WATCHER = True # Enable/disable folder monitoring
```
- **Both Modes**: Default setting; GUI runs in foreground, watcher in background.
- **GUI Only**: Set `ENABLE_WATCHER = False`.
- **Watcher Only**: Set `ENABLE_GUI = False`.
- **Neither**: Set both to `False` (exits with message).

## Example Output
```
Press 'p' to paste, 's' to select, or 'q' to quit: 
Uploaded & copied to clipboard: ![](https://i.imgur.com/abc123.png) (from folder watcher)
Press 'p' to paste, 's' to select, or 'q' to quit: p
Uploaded & copied to clipboard: ![](https://i.imgur.com/xyz789.png)
Returning to menu...
Press 'p' to paste, 's' to select, or 'q' to quit: q
Exiting...
```

## Requirements
Listed in `requirements.txt`:
```
requests
Pillow
pyperclip
watchdog
```
- **Python**: 3.6 or higher.
- **OS**: Tested on Linux (Kali); should work on Windows/Mac with Tkinter and clipboard support.
- **Dependencies**: Install via `pip install -r requirements.txt`.
- **Clipboard**: Requires `xclip` or similar on Linux for clipboard pasting.

## Troubleshooting
- **No Downloads Folder**: Ensure `~/Downloads` exists (`mkdir ~/Downloads`). The script defaults to `~` if missing.
- **Network Errors**: Check internet (`ping api.imgur.com`). For DNS issues, try `nameserver 8.8.8.8` in `/etc/resolv.conf`.
- **Invalid Client ID**: If HTTP 401 errors occur, get a new Imgur Client ID.
- **Clipboard Issues**: Ensure an image is copied (right-click > Copy Image). Install `xclip` on Linux if needed.
- **GUI Errors**: Install Tkinter (`sudo apt-get install python3-tk`).

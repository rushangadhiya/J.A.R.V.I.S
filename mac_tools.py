
import subprocess


ALLOWED_APPS = {
    # Browsers
    "safari": "Safari",
    "chrome": "Google Chrome",
    "atlas": "ChatGPT Atlas",

    # AI assistants
    "chatgpt": "ChatGPT",
    "claude": "Claude",
    "ollama": "Ollama",
    "antigravity": "Antigravity",
    "opencode": "OpenCode",

    # Development
    "vscode": "Visual Studio Code",
    "visual studio": "Visual Studio",
    "xcode": "Xcode",
    "intellij": "IntelliJ IDEA CE",
    "android studio": "Android Studio",
    "docker": "Docker",
    "github": "GitHub Desktop",
    "github desktop": "GitHub Desktop",
    "postman": "Postman",
    "terminal": "Terminal",
    "idle": "IDLE",
    "python launcher": "Python Launcher",
    "r": "R",
    "rstudio": "RStudio",

    # Microsoft Office
    "word": "Microsoft Word",
    "excel": "Microsoft Excel",
    "powerpoint": "Microsoft PowerPoint",
    "onenote": "Microsoft OneNote",

    # Apple productivity
    "pages": "Pages",
    "numbers": "Numbers",
    "keynote": "Keynote",
    "notes": "Notes",
    "notability": "Notability",
    "calendar": "Calendar",
    "reminders": "Reminders",
    "freeform": "Freeform",
    "shortcuts": "Shortcuts",
    "mail": "Mail",
    "contacts": "Contacts",
    "messages": "Messages",
    "facetime": "FaceTime",
    "phone": "Phone",
    "clock": "Clock",
    "calculator": "Calculator",
    "textedit": "TextEdit",
    "preview": "Preview",

    # Communication
    "whatsapp": "WhatsApp",
    "zoom": "zoom.us",
    "teams": "Microsoft Teams",
    "webex": "Webex",

    # Music and entertainment
    "spotify": "Spotify",
    "music": "Music",
    "apple music": "Music",
    "podcasts": "Podcasts",
    "tv": "TV",
    "books": "Books",
    "quicktime": "QuickTime Player",
    "imovie": "iMovie",
    "garageband": "GarageBand",
    "mkplayer": "MKPlayer",

    # Photos and creative tools
    "photos": "Photos",
    "photo booth": "Photo Booth",
    "image playground": "Image Playground",
    "iwallpaper": "iwallpaper",
    "wacom": "Wacom Center",

    # macOS utilities
    "finder": "Finder",
    "settings": "System Settings",
    "system settings": "System Settings",
    "activity monitor": "Activity Monitor",
    "disk utility": "Disk Utility",
    "console": "Console",
    "system information": "System Information",
    "screenshot": "Screenshot",
    "font book": "Font Book",
    "screen sharing": "Screen Sharing",
    "automator": "Automator",

    # Other useful applications
    "maps": "Maps",
    "weather": "Weather",
    "app store": "App Store",
    "find my": "FindMy",
    "passwords": "Passwords",
    "cloudflare": "Cloudflare WARP",
    "warp": "Cloudflare WARP",
    "iphone mirroring": "iPhone Mirroring",
}



def open_application(app_name: str):
    """Open an approved macOS application by name."""

    app = ALLOWED_APPS.get(app_name.strip().lower())

    if app is None:
        return {
            "success": False,
            "error": f"Application '{app_name}' is not approved."
        }

    result = subprocess.run(
        ["open", app] if app.endswith(".app") else ["open", "-a", app],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "success": False,
            "error": result.stderr.strip()
        }

    return {
        "success": True,
        "application": app
    }

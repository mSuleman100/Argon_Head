import subprocess
import re


def get_screen_size():
    """Detect screen resolution using fbset (for Raspberry Pi framebuffer)."""
    try:
        output = subprocess.check_output(['fbset', '-s']).decode()
        match = re.search(r'mode "(\d+)x(\d+)"', output)
        if match:
            width, height = int(match.group(1)), int(match.group(2))
            return width, height
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Fallback to tkinter detection
    try:
        import tkinter as tk
        root = tk.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height
    except Exception:
        pass

    # Default fallback
    return 1024, 768

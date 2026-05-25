import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import threading
import time
import os
from api.screen import get_screen_size

window = None
label_text = None
label_image = None
display_lock = threading.Lock()
IDLE_IMAGE_PATH = "media/images/robot_idle.png"


def _init_window():
    global window, label_text, label_image

    try:
        window = tk.Tk()
        window.title("Argon Kiosk Display")
        window.attributes('-fullscreen', True)  # Fullscreen mode

        width, height = get_screen_size()
        window.geometry(f"{width}x{height}")

        # Create a frame to hold image and text
        frame = tk.Frame(window, bg="black")
        frame.pack(expand=True, fill="both")

        # Image label (background)
        label_image = tk.Label(frame, bg="black")
        label_image.pack(expand=True, fill="both")

        # Text label (overlay)
        label_text = tk.Label(
            frame,
            text="",
            font=("Arial", 60),
            fg="white",
            bg="black",
            wraplength=width - 100
        )
        label_text.pack(expand=True, fill="both")

        window.configure(bg="black")

        # Load and display idle image
        if os.path.exists(IDLE_IMAGE_PATH):
            try:
                img = Image.open(IDLE_IMAGE_PATH)
                # Resize image to fit screen
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                label_image.config(image=photo)
                label_image.image = photo  # Keep a reference
            except Exception as e:
                print(f"Error loading image: {e}")

        # Start the event loop
        window.mainloop()
    except Exception as e:
        print(f"Display initialization error: {e}")


def start_display():
    """Start the display window in a separate thread"""
    global window

    if window is None:
        thread = threading.Thread(target=_init_window, daemon=False)
        thread.start()
        time.sleep(1)  # Give window time to initialize


def show_message(text: str, duration: int = 3):
    """Display a message on the kiosk"""
    global label_text, window

    with display_lock:
        # Initialize display if needed
        if window is None:
            start_display()

        if label_text is not None:
            try:
                # Update text
                def update_text():
                    try:
                        label_text.config(text=text)

                        # Schedule clear after duration
                        if duration > 0:
                            label_text.after(duration * 1000, lambda: label_text.config(text=""))
                    except tk.TclError as e:
                        print(f"Display error: {e}")

                label_text.after(0, update_text)
            except Exception as e:
                print(f"Error: {e}")
                print(f"Display message: {text}")
        else:
            print(f"Display message: {text}")

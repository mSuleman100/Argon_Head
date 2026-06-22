import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
import os
from api.screen import get_screen_size

window = None
label_text = None
label_image = None
display_lock = threading.Lock()
IMAGE_DIR = "media/images"
IDLE_IMAGE_PATH = f"{IMAGE_DIR}/robot_idle.png"
_current_photo = None


def _init_window():
    global window, label_text, label_image

    try:
        window = tk.Tk()
        window.title("Argon Kiosk Display")
        window.attributes('-fullscreen', True)  # Fullscreen mode

        width, height = get_screen_size()
        window.geometry(f"{width}x{height}")

        # Frame fills the screen; image and text are layered with place()
        frame = tk.Frame(window, bg="black")
        frame.pack(expand=True, fill="both")

        label_image = tk.Label(frame, bg="black")
        label_image.place(x=0, y=0, relwidth=1, relheight=1)

        label_text = tk.Label(
            frame,
            text="",
            font=("Arial", 60),
            fg="white",
            bg="black",
            wraplength=width - 100,
        )
        label_text.place(relx=0.5, rely=0.5, anchor="center")

        window.configure(bg="black")

        # Load and display idle image
        if os.path.exists(IDLE_IMAGE_PATH):
            try:
                photo = _load_image_photo(IDLE_IMAGE_PATH, width, height)
                _set_label_image(photo)
            except Exception as e:
                print(f"Error loading image: {e}")

        # Start the event loop
        window.mainloop()
    except Exception as e:
        print(f"Display initialization error: {e}")


def _load_image_photo(path: str, width: int, height: int):
    img = Image.open(path)
    img.thumbnail((width, height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)


def _set_label_image(photo):
    global _current_photo
    _current_photo = photo
    label_image.config(image=photo)
    label_image.image = photo


def _restore_idle_image():
    global _current_photo

    if label_image is None or window is None:
        return

    if not os.path.exists(IDLE_IMAGE_PATH):
        _current_photo = None
        label_image.config(image="")
        label_image.image = None
        return

    try:
        width, height = get_screen_size()
        photo = _load_image_photo(IDLE_IMAGE_PATH, width, height)
        _set_label_image(photo)
    except Exception as e:
        print(f"Error restoring idle image: {e}")


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
        if window is None:
            start_display()

        for _ in range(30):
            if label_text is not None:
                break
            time.sleep(0.1)

        if label_text is not None:
            try:
                # Update text
                def update_text():
                    try:
                        label_text.config(text=text)
                        label_text.lift()

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


def show_image(file: str, duration: int = 0):
    """Display an image on the kiosk."""
    global label_image, window

    path = os.path.join(IMAGE_DIR, file)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")

    with display_lock:
        if window is None:
            start_display()

        if label_image is None:
            print(f"Display image: {path}")
            return

        def update_image():
            try:
                width, height = get_screen_size()
                photo = _load_image_photo(path, width, height)
                _set_label_image(photo)
                if label_text is not None:
                    label_text.lift()

                if duration > 0:
                    label_image.after(duration * 1000, _restore_idle_image)
            except tk.TclError as e:
                print(f"Display error: {e}")
            except Exception as e:
                print(f"Error loading image: {e}")

        label_image.after(0, update_image)

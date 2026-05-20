import tkinter as tk
import threading

window = None
label = None


def _init_window():
    global window, label

    window = tk.Tk()
    window.title("Robot Display")
    window.geometry("800x480")  # good for Raspberry Pi screen

    label = tk.Label(
        window,
        text="",
        font=("Arial", 40),
        fg="white",
        bg="black"
    )
    label.pack(expand=True, fill="both")

    window.configure(bg="black")
    window.mainloop()


def start_display():
    thread = threading.Thread(target=_init_window, daemon=True)
    thread.start()


def show_message(text: str):
    global label

    if label is None:
        start_display()

    # update text safely
    def update():
        label.config(text=text)

    label.after(0, update)
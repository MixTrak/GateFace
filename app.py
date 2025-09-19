import os
import cv2
import subprocess
import tkinter as tk
from skimage.metrics import structural_similarity as ssim

# ------------------------
# Config
# ------------------------
URLS = [
    "https://music.youtube.com",
    "https://github.com/MixTrak",
]
CHROME = "Google Chrome"

REFERENCE_IMAGE = "img.jpg"
TEMP_IMAGE = "photo.jpg"
THRESHOLD = 0.7

# ------------------------
# Logic
# ------------------------
def capture():
    cam = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # macOS backend
    if not cam.isOpened():
        raise RuntimeError("Could not open webcam. Check System Settings.")
    for _ in range(10):  # warm-up frames
        ret, frame = cam.read()
    cam.release()
    if not ret:
        raise RuntimeError("Capture failed.")
    return frame

def compare(img1, img2):
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    score, _ = ssim(img1, img2, full=True)
    return score

def run(status_label):
    try:
        frame = capture()

        if not os.path.exists(REFERENCE_IMAGE):
            cv2.imwrite(REFERENCE_IMAGE, frame)
            status_label.config(
                text="No reference found. Saved first photo.",
                fg="yellow"
            )
            return

        cv2.imwrite(TEMP_IMAGE, frame)
        ref = cv2.imread(REFERENCE_IMAGE, cv2.IMREAD_GRAYSCALE)
        new = cv2.imread(TEMP_IMAGE, cv2.IMREAD_GRAYSCALE)

        score = compare(ref, new)
        os.remove(TEMP_IMAGE)

        if score >= THRESHOLD:
            status_label.config(
                text=f"Similarity {score*100:.1f}% → Launching apps...",
                fg="lightgreen"
            )
            subprocess.run(["open", "-a", CHROME, *URLS])
        else:
            status_label.config(
                text=f"Similarity {score*100:.1f}% → Images differ.",
                fg="red"
            )
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="orange")

# ------------------------
# Tkinter UI
# ------------------------
def gui():
    root = tk.Tk()
    root.title("Face Match App")
    root.geometry("460x260")
    root.configure(bg="#1e1e2f")  # dark theme
    root.attributes("-topmost", True)

    # Title
    tk.Label(
        root,
        text="Face Match & App Launcher",
        font=("Helvetica", 16, "bold"),
        bg="#1e1e2f",
        fg="white"
    ).pack(pady=20)

    # Buttons frame
    btn_frame = tk.Frame(root, bg="#1e1e2f")
    btn_frame.pack(pady=20)

    status_label = tk.Label(
        root,
        text="Waiting...",
        font=("Helvetica", 13),
        bg="#1e1e2f",
        fg="white"
    )
    status_label.pack(pady=10)

    run_btn = tk.Button(
        btn_frame,
        text="Run Face Match",
        font=("Helvetica", 13, "bold"),
        bg="#4CAF50", fg="white",
        activebackground="#45a049",
        activeforeground="black",
        width=18, height=2,
        command=lambda: run(status_label)
    )
    run_btn.grid(row=0, column=0, padx=10)

    quit_btn = tk.Button(
        btn_frame,
        text="Exit",
        font=("Helvetica", 13, "bold"),
        bg="#f44336", fg="white",
        activebackground="#e53935",
        activeforeground="black",
        width=10, height=2,
        command=root.quit
    )
    quit_btn.grid(row=0, column=1, padx=10)

    root.mainloop()

if __name__ == "__main__":
    gui()

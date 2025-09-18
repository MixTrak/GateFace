import sys
import os
import traceback
import tkinter as tk
from tkinter import messagebox
import cv2
from skimage.metrics import structural_similarity as ssim
import subprocess

# ------------------------
# Error Logging (Step 1)
# ------------------------
def excepthook(exc_type, exc_value, exc_traceback):
    """Log uncaught exceptions to error.log"""
    with open("error.log", "w") as f:
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
sys.excepthook = excepthook

# ------------------------
# Configuration
# ------------------------

URLS = [
    "https://www.google.com",
]

APPLICATIONS = { 
    "chrome": "/Applications/Google Chrome.app",
}

REFERENCE_IMAGE = "img.jpg"
TEMP_IMAGE = "photo.jpg"

SIMILARITY_THRESHOLD = 0.7

# ------------------------
# Functions
# ------------------------

def capture_photo():
    """Capture a photo from the default webcam."""
    cam = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # Step 2: macOS backend

    if not cam.isOpened():
        raise RuntimeError("❌ Could not open webcam. Check camera permissions in System Settings.")

    for _ in range(10):  # warm-up frames
        ret, frame = cam.read()
    cam.release()

    if not ret:
        raise RuntimeError("❌ Failed to capture image from camera.")
    return frame


def save_image(path, image):
    cv2.imwrite(path, image)


def load_grayscale(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Failed to read image: {path}")
    return img


def compare_images(img1, img2):
    """Compare two images using SSIM and return similarity score (0-1)."""
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    score, _ = ssim(img1, img2, full=True)
    return score


def launch_apps():
    """Launch configured apps and URLs."""
    subprocess.run(["open", "-a", APPLICATIONS["chrome"], *URLS])


def main_logic():
    try:
        frame = capture_photo()

        if not os.path.exists(REFERENCE_IMAGE):
            save_image(REFERENCE_IMAGE, frame)
            messagebox.showinfo("Info", f"No existing reference image found.\nSaved first photo as {REFERENCE_IMAGE}")
            return

        save_image(TEMP_IMAGE, frame)

        reference_img = load_grayscale(REFERENCE_IMAGE)
        new_img = load_grayscale(TEMP_IMAGE)

        similarity = compare_images(reference_img, new_img)
        result_text = f"Similarity score: {similarity*100:.2f}%"

        if similarity >= SIMILARITY_THRESHOLD:
            messagebox.showinfo("Result", f"{result_text}\n\n✅ Images Are Similar.\nLaunching Apps...")
            launch_apps()
        else:
            messagebox.showwarning("Result", f"{result_text}\n\n❌ Images Are Different.")

        os.remove(TEMP_IMAGE)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ------------------------
# Tkinter GUI
# ------------------------

def create_gui():
    root = tk.Tk()
    root.title("Face Match App")
    root.geometry("400x200")

    # Force window to always be on top
    root.attributes("-topmost", True)

    label = tk.Label(root, text="Face Match & App Launcher", font=("Arial", 14))
    label.pack(pady=20)

    run_button = tk.Button(root, text="Run Face Match", font=("Arial", 12), command=main_logic)
    run_button.pack(pady=10)

    quit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=root.quit)
    quit_button.pack(pady=10)

    print("✅ GUI started")
    root.mainloop()


if __name__ == "__main__":
    create_gui()

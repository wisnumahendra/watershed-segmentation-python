import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import image_processing 

def choose_image():
    global original_image
    global img_label
    global processed_label

    image_path = filedialog.askopenfilename()
    if image_path:
        original_image = cv2.imread(image_path)
        show_image(original_image)

def show_image(image):
    global img_label

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)

    if img_label is None:
        img_label = tk.Label(root, image=img, borderwidth=2, relief="groove")
        img_label.image = img
        img_label.pack(padx=10, pady=5)
    else:
        img_label.configure(image=img)
        img_label.image = img

def process_image():
    global original_image

    if original_image is not None:
        processed_image = image_processing.apply_watershed(original_image)
        show_processed_image(processed_image)

def show_processed_image(image):
    global processed_label

    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    processed_img = Image.fromarray(processed_img)
    processed_img = ImageTk.PhotoImage(processed_img)

    if processed_label is None:
        processed_label = tk.Label(root, image=processed_img, borderwidth=2, relief="groove")
        processed_label.image = processed_img
        processed_label.pack(padx=10, pady=5)
    else:
        processed_label.configure(image=processed_img)
        processed_label.image = processed_img

root = tk.Tk()
root.title("Image Processing")

original_image = None
img_label = None
processed_label = None

choose_button = tk.Button(root, text="Choose Image", command=choose_image, bg="#4CAF50", fg="white", padx=10, pady=5)
choose_button.pack(padx=10, pady=5)

process_button = tk.Button(root, text="Watershed Process", command=process_image, bg="#008CBA", fg="white", padx=10, pady=5)
process_button.pack(padx=10, pady=5)

root.mainloop()

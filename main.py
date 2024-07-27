'''main'''

import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

# Function to colorize the image or video
def colorize_image():
    # Load the selected image or video
    file_path = filedialog.askopenfilename()
    if file_path:
        if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')):
            colorize_video(file_path)
        else:
            colorize_image_file(file_path)

# Function to colorize an image file
def colorize_image_file(file_path):
    image = cv2.imread(file_path)
    colorized = colorize(image)
    display_original(image)
    display_colorized(colorized)

# Function to colorize a video
def colorize_video(file_path):
    cap = cv2.VideoCapture(file_path)
    '''fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('colorized_video.avi', fourcc, 30, (600, 450))'''
    # Change the codec to H264 and the output file extension to .mp4
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    out = cv2.VideoWriter('colorized_video.mp4', fourcc, 30, (600, 450))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        colorized_frame = colorize(frame)
        cv2.imshow("Original Video", frame)
        cv2.imshow("Colorized Video", colorized_frame)
        out.write(colorized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    out.release()
    cap.release()
    cv2.destroyAllWindows()

# Function to save colorized image
def save_colorized_image(colorized):
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
    if file_path:
        cv2.imwrite(file_path, colorized)

# Function to save colorized video in MP4 format
def save_colorized_video_mp4():
    file_path = filedialog.asksaveasfilename(defaultextension=".mp4")
    if file_path:
        cap = cv2.VideoCapture('colorized_video.avi')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use mp4v for MP4 format
        out = cv2.VideoWriter(file_path, fourcc, 30, (600, 450))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        out.release()
        cap.release()
    os.remove('colorized_video.avi')

# Function to colorize an image
def colorize(image):
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    # Load the colorization model (same code as before)
    DIR = r""  # Your model directory
    PROTOTXT = os.path.join(DIR, r"model/colorization_deploy_v2.prototxt")
    POINTS = os.path.join(DIR, r"model/pts_in_hull.npy")
    MODEL = os.path.join(DIR, r"model/colorization_release_v2.caffemodel")

    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
    pts = np.load(POINTS)

    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)

    colorized = (255 * colorized).astype("uint8")
    return colorized

# Function to display the original image
def display_original(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = img.resize((600, 450), Image.LANCZOS)  # Resize the image (adjust size as needed)
    img = ImageTk.PhotoImage(img)
    original_label.config(image=img)
    original_label.image = img

# Function to display the colorized image
def display_colorized(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = img.resize((600, 450), Image.LANCZOS)  # Resize the image (adjust size as needed)
    img = ImageTk.PhotoImage(img)
    colorized_label.config(image=img)
    colorized_label.image = img

# Create the main application window
app = tk.Tk()
app.title("Image/Video Colorization App")
app.geometry("1400x600")  # Set the initial window size (adjust as needed)

# Stylish custom colors
bg_color = "#333333"
button_color = "#4CAF50"
text_color = "white"
font_style = ("Helvetica", 14)

# Create a label for the app title with gap
title_label = tk.Label(
    app,
    text="Image/Video Colorization App",
    font=("Helvetica", 24),
    bg=bg_color,
    fg="white",
    pady=20,
)
title_label.pack()

# Create a frame to contain the buttons and images
frame = tk.Frame(app, bg=bg_color)
frame.pack(pady=20)

# Create a rounded button to select an image or video with custom style
# ... (previous code)
select_button = tk.Button(
    frame,
    text="Select Image/Video",
    command=colorize_image,
    font=font_style,
    bg=button_color,
    fg=text_color,
    padx=20,
    pady=10,
    relief=tk.RIDGE,  # Add relief for a curved button
    borderwidth=3,    # Border width for better visibility
    width=20,         # Set the button width
)
select_button.pack()

# Create a "Save" button for images
save_image_button = tk.Button(
    frame,
    text="Save Image",
    command=lambda: save_colorized_image(colorized_label.image),
    font=font_style,
    bg=button_color,
    fg=text_color,
    padx=20,
    pady=10,
    relief=tk.RIDGE,
    borderwidth=3,
    width=20,
)
save_image_button.pack()

# ... (rest of the code)

# Create a "Save" button for images
# Create a "Save" button for images
'''save_image_button = tk.Button(
    frame,
    text="Save Image",
    command=lambda: save_colorized_image(colorized_image),
    font=font_style,
    bg=button_color,
    fg=text_color,
    padx=20,
    pady=10,
    relief=tk.RIDGE,
    borderwidth=3,
    width=20,
)
save_image_button.pack()'''

# Create a "Save" button for videos in MP4 format
    # Create a "Save" button for videos in MP4 format
save_video_mp4_button = tk.Button(
    frame,
    text="Save Video (MP4)",
    command=save_colorized_video_mp4,
    font=font_style,
    bg=button_color,
    fg=text_color,
    padx=20,
    pady=10,
    relief=tk.RIDGE,
    borderwidth=3,
    width=20,
)
save_video_mp4_button.pack()

    # Add spacing
spacer = tk.Label(frame, text="", bg=bg_color)
spacer.pack()

    # Create labels for original and colorized images (without text)
original_label = tk.Label(frame, bg=bg_color)
colorized_label = tk.Label(frame, bg=bg_color)

    # Display the original and colorized images side by side
original_label.pack(side=tk.LEFT, padx=20)
colorized_label.pack(side=tk.LEFT, padx=20)

app.mainloop()

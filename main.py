import PySimpleGUI as sg
import os
import io
from PIL import Image, ImageEnhance
import numpy as np
import img_editor

# Set theme
sg.theme("DarkBlue")

# Define layout components
first_column = [
    [sg.Text("Open Image Folder:")],
    [sg.In(size=(20, 1), enable_events=True, key="ImgFolder"), sg.FolderBrowse()],
    [sg.Text("Choose an image from list:")],
    [sg.Listbox(values=[], enable_events=True, size=(20, 10), key="ImgList")],
]

second_column = [
    [sg.Text("Image Input:")],
    [sg.Image(key="ImgInputViewer", size=(350, 350), background_color="black")],
    [sg.Button("Generate GIF", key="GenerateGIF")],
]

third_column = [
    [sg.Text("Image Output:")],
    [sg.Image(key="ImgOutputViewer", size=(350, 350), background_color="black")],
    [sg.Text("Filter:")],
    [sg.Combo(values=["Brightness", "Contrast", "Saturation", "Hue"], key="Filter", readonly=True)],
    [sg.Text("Intensity:")],
    [sg.Slider(range=(0, 2), default_value=1, resolution=0.1, orientation="h", size=(20, 15), key="Intensity")],
    [sg.Button("Apply Filter", key="ApplyFilter")],
    [sg.Button("Export", key="Export")],
]

fourth_column = [
    [sg.Text("History:")],
    [sg.Listbox(values=[], enable_events=True, size=(20, 10), key="HistoryList")],
    [sg.Button("Undo", key="Undo")],
]

layout = [
    [sg.Column(first_column), sg.VSeparator(), sg.Column(second_column), sg.VSeparator(), sg.Column(third_column), sg.VSeparator(), sg.Column(fourth_column)],
]

# Create the window
window = sg.Window("Image Editor", layout)

# Initialize variables
filename_out = "output.png"
filename_input = ""
img_input = None
layers = []
history_folder = "history"
if not os.path.exists(history_folder):
    os.makedirs(history_folder)

# Function to apply filters
def apply_filters(image, layers):
    for layer in layers:
        if layer["type"] == "Brightness":
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(layer["intensity"])
        elif layer["type"] == "Contrast":
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(layer["intensity"])
        elif layer["type"] == "Saturation":
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(layer["intensity"])
        elif layer["type"] == "Hue":
            image = image.convert('HSV')
            np_image = np.array(image)
            np_image[..., 0] = (np_image[..., 0] * layer["intensity"]).astype(np.uint8)
            image = Image.fromarray(np_image, 'HSV').convert('RGB')
    return image

# Function to save history
def save_history(image, layers, index):
    history_image_path = os.path.join(history_folder, f"history_{index}.png")
    image.save(history_image_path)
    return history_image_path

history_index = 0
history_paths = []

while True:
    event, values = window.read()
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "ImgFolder":
        folder = values["ImgFolder"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", ".jpeg"))]
        window["ImgList"].update(fnames)
    elif event == "ImgList":
        filename_input = os.path.join(values["ImgFolder"], values["ImgList"][0])
        img_input = Image.open(filename_input)
        thumbnail = img_editor.generate_preview(img_input)
        bio = io.BytesIO()
        thumbnail.save(bio, format="PNG")
        window["ImgInputViewer"].update(data=bio.getvalue())
        
        # Reset history
        layers = []
        history_index = 0
        history_paths = []
        window["HistoryList"].update(history_paths)
    elif event == "ApplyFilter":
        if img_input:
            filter_type = values["Filter"]
            intensity = values["Intensity"]
            if filter_type:
                layers.append({"type": filter_type, "intensity": intensity})
                img_output = apply_filters(img_input.copy(), layers)
                
                # Save history
                history_index += 1
                history_path = save_history(img_output, layers, history_index)
                history_paths.append(history_path)
                window["HistoryList"].update(history_paths)
                
                bio = io.BytesIO()
                thumbnail_out = img_editor.generate_preview(img_output)
                thumbnail_out.save(bio, format="PNG")
                window["ImgOutputViewer"].update(data=bio.getvalue())
    elif event == "Export":
        if img_input:
            img_output = apply_filters(img_input.copy(), layers)
            img_output.save(filename_out)
            sg.popup("Image exported successfully!", title="Export")
    elif event == "Undo":
        if len(history_paths) > 1:
            history_paths.pop()
            layers.pop()
            window["HistoryList"].update(history_paths)
            
            if history_paths:
                last_history_path = history_paths[-1]
                img_output = Image.open(last_history_path)
                bio = io.BytesIO()
                img_output.thumbnail((350, 350))
                img_output.save(bio, format="PNG")
                window["ImgOutputViewer"].update(data=bio.getvalue())
            else:
                window["ImgOutputViewer"].update(data=None)

window.close()
# clear history folder
for filename in os.listdir(history_folder):
    os.remove(os.path.join(history_folder, filename))
    
# app.py
from flask import Flask, render_template, request, jsonify
import os
import cv2
import json
import shutil
from ultralytics import YOLO

app = Flask(__name__)

model = YOLO('best.pt')  # Load the pretrained YOLOv8n model


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
results = None
names = None
image_path= []
json_str = ""

def delete_folder_and_contents(folder_path):

    
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents deleted successfully.")
    except OSError as e:
        print(f"Error deleting folder '{folder_path}': {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def wriylop(result):   # convert results to annotation format
    print("hello")
    ggh = []
    for i in range(len(result.boxes)):
            boxes = result.boxes[i]
            classnk = names[result.boxes.cls[i].item()]
            boxes.xyxy[0][1]
            aspa = {"class_name": classnk,
                    "bounding_box": {
                    "xmin": boxes.xyxy[0][0].item(),
                    "ymin": boxes.xyxy[0][1].item(),
                    "xmax": boxes.xyxy[0][2].item(),
                    "ymax": boxes.xyxy[0][3].item()
                }}
                
            ggh.append(aspa)

    img = cv2.imread(result.path)
    height, width = img.shape[:2]
    data = {
        "Name": os.path.basename(result.path),
        "image_width": width,
        "image_height": height,
        "objects": ggh
        }
        # Convert the JSON data to a string
    json_str = json.dumps(data, indent=4)
    return json_str  # Return the JSON string instead of writing it to a file



@app.route('/upload', methods=['POST'])
def upload_images(): # for the upload and classification
    global results,names,image_path, json_str
    json_str = ""
    if 'image' not in request.files:
        return jsonify({'error': 'No images provided'}), 400

    images = request.files.getlist('image')
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    else:
        delete_folder_and_contents('uploads')
        os.makedirs('uploads')
    
    if os.path.exists('static/predict'):
        delete_folder_and_contents('static/predict')
    
    filenames = []
    for image in images:
        if image and allowed_file(image.filename):
            # filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(filepath)
            print(filepath)
            image_path.append(filepath)
            print(image.filename)
            filenames.append(image.filename)

    if not filenames:
        return jsonify({'error': 'No valid image provided'}), 400

    predictions = []  # List to store the classification results
    full_predicitions = []
    predicted = []
    try:
        # Open the image using Pillow to validate its format
        

        # Perform object detection and classification on the image
        results = model("uploads/", project="static/", save=True, stream=True, conf=0.4)
        names= model.names
            # Process the results and add them to the predictions list
        for result in results:
            
            for box, conf, cls in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls):
                predictions={
                    'x_min': box[0].item(),
                    'y_min': box[1].item(),
                    'x_max': box[2].item(),
                    'y_max': box[3].item(),
                    'confidence': conf.item(),
                    'class': int(cls.item()),
                }
                predicted.append(predictions)
           
            # print( predictions)
            json_str += wriylop(result)
            filename = os.path.basename(result.path)
            full_predicitions.append([filename,predicted])
            # print(full_predicitions)
            predicted =[]
            
        return jsonify({'predictions': full_predicitions})
    except Exception as e:
        return jsonify({'error': 'Error processing image: {}'.format(e)}), 400

    return render_template('index.html')


@app.route('/get_images')
def get_images():
    image_folder = 'static/predict'  # Replace with the actual path to your folder
    image_paths = []

    # Loop through all files in the image folder and check if they are image files
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_folder, filename)
            image_paths.append(image_path)
            
    return jsonify(image_paths)


@app.route('/download_file')
def download_file():
    global json_str

    try:
        return json_str
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/', methods=['GET', 'POST'])
def upload_and_classify():


    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

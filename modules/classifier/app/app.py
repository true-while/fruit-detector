import json
import os
import io

from azure.storage.blob import BlobServiceClient
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

# Imports for the REST API
from flask import Flask, request, jsonify

# Imports for image procesing
from PIL import Image

# Imports for prediction
from predict import initialize, predict_image, predict_url

app = Flask(__name__)

# 4MB Max image size limit
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 

# Default route just shows simple text
@app.route('/')
def index():
    return 'CustomVision.ai model host harness'

# Like the CustomVision.ai Prediction service /image route handles either
#     - octet-stream image file 
#     - a multipart/form-data with files in the imageData parameter
@app.route('/image', methods=['POST'])
@app.route('/<project>/image', methods=['POST'])
@app.route('/<project>/image/nostore', methods=['POST'])
@app.route('/<project>/classify/iterations/<publishedName>/image', methods=['POST'])
@app.route('/<project>/classify/iterations/<publishedName>/image/nostore', methods=['POST'])
@app.route('/<project>/detect/iterations/<publishedName>/image', methods=['POST'])
@app.route('/<project>/detect/iterations/<publishedName>/image/nostore', methods=['POST'])
def predict_image_handler(project=None, publishedName=None):
    try:
        imageData = None
        if ('imageData' in request.files):
            imageData = request.files['imageData']
        elif ('imageData' in request.form):
            imageData = request.form['imageData']
        else:
            imageData = io.BytesIO(request.get_data())

        img = Image.open(imageData)

        src_filename = 'output.png'
        dst_filename = 'analyzed.png'
        img.save(src_filename, "PNG")

        print('Upload img')
        upload(src_filename)

        results = predict_image(img)

        print('Create borders')
        draw_borders(img, results, src_filename, dst_filename)

        print('Upload results')
        upload(dst_filename)    

        return jsonify(results)

    except Exception as e:
        print('EXCEPTION:', str(e))
        return 'Error processing image', 500


# Like the CustomVision.ai Prediction service /url route handles url's
# in the body of hte request of the form:
#     { 'Url': '<http url>'}  
@app.route('/url', methods=['POST'])
@app.route('/<project>/url', methods=['POST'])
@app.route('/<project>/url/nostore', methods=['POST'])
@app.route('/<project>/classify/iterations/<publishedName>/url', methods=['POST'])
@app.route('/<project>/classify/iterations/<publishedName>/url/nostore', methods=['POST'])
@app.route('/<project>/detect/iterations/<publishedName>/url', methods=['POST'])
@app.route('/<project>/detect/iterations/<publishedName>/url/nostore', methods=['POST'])
def predict_url_handler(project=None, publishedName=None):
    try:
        image_url = json.loads(request.get_data().decode('utf-8'))['url']
        results = predict_url(image_url)
        return jsonify(results)
    except Exception as e:
        print('EXCEPTION:', str(e))
        return 'Error processing image'

def upload(local_file_name):

    container_name = 'camtaken'
    account_name = os.environ.get('BLOB_ACC')
    account_key = os.environ.get('BLOB_KEY')
    connection_string = ("DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net").format(account_name,account_key)
    print("connect: " + connection_string)
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)

    blob_service_client.create_container(container_name)

    local_path = os.path.expanduser("./")

    if not os.path.exists(local_path):
        os.makedirs(os.path.expanduser("./"))

    full_path_to_file = os.path.join(local_path, local_file_name)

    print("\nUploading to Blob storage as blob" + local_file_name)

    blob_service_client.create_blob_from_path(container_name, local_file_name, full_path_to_file)


def draw_borders(img, analysis, input_file, dest_file):
    img = Image.open(input_file)
    test_img_w, test_img_h = img.size

    object_colors = {
        "apple": "lightgreen",
        "banana": "yellow",
        "orange": "orange"
    }
    draw = ImageDraw.Draw(img)

    for prediction in analysis.predictions:
        color = 'white' # default for 'other' object tags
        if (prediction.probability*100) > 50:
            if prediction.tagName in object_colors:
                color = object_colors[prediction.tagName]
            left = prediction.boundingBox.left * test_img_w 
            top = prediction.boundingBox.top * test_img_h 
            height = prediction.boundingBox.height * test_img_h
            width =  prediction.boundingBox.width * test_img_w
            points = ((left,top), (left+width,top), (left+width,top+height), (left,top+height),(left,top))
            draw.line(points, fill=color, width=3)
            draw.rectangle(((left,top-30), (left+width,top-2)), fill=color)
            draw.text((left+2, top-28), prediction.tagName + "\n{0:.2f}%".format(prediction.probability * 100), fill='black', font=ImageFont.truetype("arial"))
 
    img.save(dest_file, "PNG")
    print('done img')

if __name__ == '__main__':
    # Load and intialize the model
    initialize()

    # Run the server
    app.run(host='0.0.0.0', port=80)


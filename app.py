import flask
from flask import request, jsonify
import os
from PIL import Image
import imagehash
import numpy as np

directory = os.getcwd()
image_dir='\dataset'
hash_size=8
threshold = 0.2
diff_limit = int(threshold*(hash_size**2))

app = flask.Flask(__name__)
app.config["DEBUG"] = True

ALLOWED_EXTENSIONS=set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS              


@app.route('/check-if-duplicate', methods=['POST'])
def upload_file():        
    if 'image' not in request.files:
        return jsonify({
            'status':False,
            'message':"No image detected"
            }),400
    file = request.files['image']
    if file.filename == '':
        return jsonify({
            'status':False,
            'message':"No image detected"
            }),400
    if file and allowed_file(file.filename):
        dataset_path=directory+image_dir
        dataset_names=os.listdir(dataset_path)
        diffarr=[]
        app.logger.debug("Image acquired")
        with Image.open(file) as img:
            hash1 = imagehash.average_hash(img, hash_size).hash        
        for image in dataset_names:
            with Image.open(os.path.join(dataset_path,image)) as img:
                hash2 = imagehash.average_hash(img, hash_size).hash
                diff=np.count_nonzero(hash1 != hash2)
                if diff <= diff_limit:
                    diffarr.append({"file":image,"score":(100-diff)/100})
                    app.logger.info("{} image found {}% similar".format(image,100-diff))  
        app.logger.debug(diffarr)
        if len(diffarr) > 0:
            return jsonify({
                'status':True,
                'message':"Image uploaded",
                'similar_images':diffarr,
                'threshold':threshold
                }),200
        return jsonify({
            'status':False,
            'message':"No similar images found"
            }),200    
    return jsonify({
        'status':False,
        'message':"Incorrect file uploaded"
        }),400 

app.run()
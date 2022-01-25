import flask
from flask import request, jsonify
import os
from PIL import Image
import imagehash
import numpy as np

directory = os.getcwd()
image_dir='\dataset'
hash_size=8

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/check-if-duplicate', methods=['GET'])
def checkIfDuplicate():
    dataset_path=directory+image_dir
    dataset_names=os.listdir(dataset_path)
    threshold = 0.2
    isduplicate=False
    diff_limit = int(threshold*(hash_size**2))
    
    with Image.open(directory+"\image-3.jpg") as img:
        hash1 = imagehash.average_hash(img, hash_size).hash
    
    print("Finding Similar Images to {} Now!\n".format(directory+"\image-3.jpg"))
    for image in dataset_names:
        with Image.open(os.path.join(dataset_path,image)) as img:
            hash2 = imagehash.average_hash(img, hash_size).hash
            if np.count_nonzero(hash1 != hash2) <= diff_limit:
                isduplicate=True
                print("{} image found {}% similar".format(image,80,directory+"\image-3.jpg"))


    return  jsonify(isduplicate=isduplicate)



app.run()
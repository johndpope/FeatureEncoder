from flask import Flask, jsonify, request, abort

import os
import numbers
import json
import base64


from fee import run

webservice = Flask(__name__)

@webservice.route('/featureencoder', methods=['POST'])
def create_new_employee():
    print(request)
    if not request.json or not 'image' in request.json:
        abort(400, "Post JSON with property image")
    
    # 
    image_decoded = request.json['image']
    input_image = base64.b64decode(image_decoded)
    if not os.path.exists("temp"):
        os.mkdir("temp")
    
    image_path = "temp/image.png"
    with open(image_path , 'wb') as file:
        file.write(input_image)
        
    # Validationdd
    #if not isinstance(input_image, numbers.Number) :
    #    abort(400, "image should be a number")
    latentspace = run(image_path)
    #print(latent_space.shape)
    #["0": [18, 512]]
    #for item in latentspace.items():
    #    print("Key", item[0])
    #    print("values  shape: ", item[1])
        
    latentspace_list = latentspace[0][0][len(latentspace[0])-1].tolist()

    latentspace_list_str = json.dumps(latentspace_list)
    
    return jsonify({'latentspace': latentspace_list_str}), 200

if __name__ == '__main__':
    webservice.run(debug=False, use_reloader=False)
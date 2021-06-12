from flask import Flask, jsonify, request, abort

import numbers

from fee import run

webservice = Flask(__name__)

@webservice.route('/featureencoder', methods=['POST'])
def create_new_employee():
    if not request.json or not 'image' in request.json:
        abort(400, "Post JSON with property image")
    
    # 
    input_image = request.json['image']

    # Validationdd
    if not isinstance(input_image, numbers.Number) :
        abort(400, "image should be a number")
    
    latentspace = run(input_image)

    return jsonify({'latentspace': latentspace}), 200

if __name__ == '__main__':
    webservice.run(debug=False, use_reloader=False)
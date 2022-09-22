# Important imports
from app import app
from flask import request, render_template
from app.utils.image_treatment import ImageTreatment
from PIL import Image
from app.utils.parameters_parser import AppParameters
import json

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():
	
	params=AppParameters().load(json.load(open('app/parameters.json')))


	if request.method == "GET":
		return render_template("index.html", full_filename = params['full_filename'])

	if request.method == "POST":

		image = Image.open(request.files['image_upload']).resize((450,250))
		print(image)
		result = ImageTreatment(image=image).fit_transform()

		return render_template('index.html', full_filename = result['full_filename'], pred = result['result'])

# Main function
if __name__ == '__main__':
    app.run(debug=True)

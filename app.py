

# from flask import Flask, render_template, request
# import os
# from pdf_image_search import search_image_in_pdfs  # Import the search function
# from PIL import Image
# import io

# app = Flask(__name__)

# # Ensure the 'uploads' directory exists
# UPLOAD_FOLDER = 'uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/', methods=['GET'])
# def index():
#     return render_template('index.html')

# @app.route('/search', methods=['POST'])
# def search():
#     # Check if files are in the request
#     if 'pdf_file' not in request.files or 'image_file' not in request.files:
#         return "No file part", 400

#     # Get the files from the request
#     pdf_file = request.files['pdf_file']
#     image_file = request.files['image_file']

#     # Check if files have been selected
#     if pdf_file.filename == '' or image_file.filename == '':
#         return "No selected file", 400

#     # Save the uploaded image to the 'uploads' directory
#     image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
#     image_file.save(image_path)

#     # Load the image directly from the saved file
#     target_image = Image.open(image_path)

#     # Save the PDF file temporarily
#     pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
#     pdf_file.save(pdf_path)

#     # Call the function to search for the image in the PDF
#     results = search_image_in_pdfs([pdf_path], target_image)

#     # If matches are found, return the results, otherwise show no matches
#     if results:
#         return render_template('results.html', results=results)
#     else:
#         return render_template('no_results.html')

# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, render_template, request, after_this_request
import os
from pdf_image_search import search_image_in_pdfs
from PIL import Image

app = Flask(__name__)

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Check if files are in the request
    if 'pdf_file' not in request.files or 'image_file' not in request.files:
        return "No file part", 400

    # Get the files from the request
    pdf_file = request.files['pdf_file']
    image_file = request.files['image_file']

    # Check if files have been selected
    if pdf_file.filename == '' or image_file.filename == '':
        return "No selected file", 400

    # Save the uploaded image to the 'uploads' directory
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(image_path)

    # Load the image directly from the saved file
    target_image = Image.open(image_path)

    # Save the PDF file temporarily
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)

    # Call the function to search for the image in the PDF
    results = search_image_in_pdfs([pdf_path], target_image)

    # Delete files after the response is sent
    @after_this_request
    def delete_files(response):
        try:
            # Remove the uploaded PDF and image files
            os.remove(pdf_path)
            os.remove(image_path)
        except Exception as e:
            print(f"Error deleting files: {e}")
        return response

    # If matches are found, return the results, otherwise show no matches
    if results:
        return render_template('results.html', results=results)
    else:
        return render_template('no_results.html')

if __name__ == "__main__":
    app.run(debug=True)

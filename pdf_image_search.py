# import fitz  # PyMuPDF
# from PIL import Image
# import numpy as np
# import io

# def extract_images_from_pdf(pdf_path):
#     """Extract images from a PDF file."""
#     pdf_images = []
#     pdf_doc = fitz.open(pdf_path)
#     for page_number in range(len(pdf_doc)):
#         page = pdf_doc[page_number]
#         image_list = page.get_images(full=True)
#         for img_index, img in enumerate(image_list):
#             xref = img[0]
#             base_image = pdf_doc.extract_image(xref)
#             image_bytes = base_image["image"]
#             image = Image.open(io.BytesIO(image_bytes))  # <-- Use io.BytesIO to handle image byte data
#             pdf_images.append((page_number + 1, image))
#     return pdf_images

# def compare_images(image1, image2, mse_threshold=80):
#     """Compare two images using Mean Squared Error (MSE)."""
#     image1 = image1.convert("RGB")
#     image2 = image2.convert("RGB")

#     # Resize images for consistency
#     image1 = image1.resize((300, 300))  
#     image2 = image2.resize((300, 300))

#     # Convert images to numpy arrays for comparison
#     image1_array = np.array(image1)
#     image2_array = np.array(image2)

#     # Compute Mean Squared Error (MSE)
#     mse = np.sum((image1_array - image2_array) ** 2) / float(image1_array.size)

#     # Debugging: Print MSE value
#     print(f"MSE: {mse}")

#     # Return True if MSE is below the threshold
#     return mse < mse_threshold

# def search_image_in_pdfs(pdf_files, target_image_path):
#     """Search for an image in multiple PDF files."""
#     target_image = Image.open(target_image_path)
#     results = []
#     for pdf_file in pdf_files:
#         print(f"Processing {pdf_file}...")
#         images = extract_images_from_pdf(pdf_file)
#         for page_num, pdf_image in images:
#             if compare_images(target_image, pdf_image):
#                 results.append((pdf_file, page_num))
#                 print(f"Match found in {pdf_file} on page {page_num}")
#     return results


import fitz  # PyMuPDF
from PIL import Image
import numpy as np
import io

def extract_images_from_pdf(pdf_path):
    """Extract images from a PDF file."""
    pdf_images = []
    pdf_doc = fitz.open(pdf_path)
    for page_number in range(len(pdf_doc)):
        page = pdf_doc[page_number]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            pdf_images.append((page_number + 1, image))
    return pdf_images

def compare_images(image1, image2, mse_threshold=80):
    """Compare two images using Mean Squared Error (MSE)."""
    image1 = image1.convert("RGB")
    image2 = image2.convert("RGB")

    # Resize images for consistency
    image1 = image1.resize((300, 300))  
    image2 = image2.resize((300, 300))

    # Convert images to numpy arrays for comparison
    image1_array = np.array(image1)
    image2_array = np.array(image2)

    # Compute Mean Squared Error (MSE)
    mse = np.sum((image1_array - image2_array) ** 2) / float(image1_array.size)

    # Debugging: Print MSE value
    print(f"MSE: {mse}")

    # Return True if MSE is below the threshold
    return mse < mse_threshold

def search_image_in_pdfs(pdf_files, target_image):
    """Search for an image in multiple PDF files."""
    results = []
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        images = extract_images_from_pdf(pdf_file)
        for page_num, pdf_image in images:
            if compare_images(target_image, pdf_image):
                results.append((pdf_file, page_num))
                print(f"Match found in {pdf_file} on page {page_num}")
    return results

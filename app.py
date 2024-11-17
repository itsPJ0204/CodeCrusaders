from flask import Flask, request, render_template
from pdf2image import convert_from_path
from PIL import Image, ImageOps, ImageFilter
import easyocr
import numpy as np
import os
import re
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Initialize EasyOCR reader with English and Hindi
reader = easyocr.Reader(['en', 'hi'])

def preprocess_image(image):
    """
    Enhance image quality for better OCR accuracy.
    """
    # Convert to grayscale
    image = image.convert("L")
    
    # Resize image to double the size for better OCR
    image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)
    
    # Apply median filter to remove noise
    image = image.filter(ImageFilter.MedianFilter())
    
    # Enhance contrast
    image = ImageOps.autocontrast(image)
    
    # Convert to NumPy array for OpenCV compatibility
    image_array = np.array(image)
    
    # Binarize the image using OpenCV (thresholding)
    _, binarized_image = cv2.threshold(image_array, 140, 255, cv2.THRESH_BINARY)
    
    # Convert back to PIL Image
    preprocessed_image = Image.fromarray(binarized_image)
    
    return preprocessed_image

def extract_text_from_file(filepath):
    """
    Extract text from an uploaded file (PDF/Image) using EasyOCR.
    """
    extracted_text = ""

    if filepath.lower().endswith(".pdf"):
        # Process PDF file
        try:
            pages = convert_from_path(filepath, 300)  # 300 DPI for high-quality images
            for page in pages:
                page = preprocess_image(page)
                page_np = np.array(page)
                results = reader.readtext(page_np)
                extracted_text += " ".join([result[1] for result in results]) + " "
        except Exception as e:
            return None, f"Error processing PDF: {str(e)}"
    else:
        # Process image file
        try:
            image = Image.open(filepath)
            image = preprocess_image(image)
            image_np = np.array(image)
            results = reader.readtext(image_np)
            extracted_text = " ".join([result[1] for result in results])
        except Exception as e:
            return None, f"Error processing image: {str(e)}"
    
    return extracted_text, None

def verhoeff_checksum(aadhar_number):
    """
    Validate an Aadhaar number using the Verhoeff checksum algorithm.
    """
    # Verhoeff algorithm tables
    d_table = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
        [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
        [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
        [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
        [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
        [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ]
    p_table = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
        [2, 8, 9, 0, 7, 1, 4, 6, 5, 3],
        [3, 9, 0, 8, 6, 4, 2, 5, 7, 1],
        [4, 0, 8, 9, 1, 3, 5, 7, 2, 6],
        [5, 7, 2, 6, 9, 0, 8, 3, 4, 1],
        [6, 4, 3, 5, 8, 2, 1, 9, 0, 7],
        [7, 3, 4, 2, 0, 6, 9, 1, 8, 5],
        [8, 6, 5, 7, 3, 9, 0, 4, 1, 2],
        [9, 2, 1, 4, 5, 7, 6, 8, 3, 0]
    ]
    inv_table = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

    # Convert Aadhaar number into a reversed list of integers
    digits = [int(d) for d in reversed(aadhar_number)]
    c = 0  # Initial checksum value

    for i in range(len(digits)):
        c = d_table[c][p_table[(i % 8)][digits[i]]]

    return c == 0

def validate_aadhar_card(text):
    aadhar_number_pattern = r"\b\d{4} \d{4} \d{4}\b"
    aadhar_number_pattern_no_space = r"\b\d{12}\b"
    name_pattern = re.compile(r"\b([A-Z]+ [A-Z]+)\b")
    dob_pattern = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")  
    address_pattern = re.compile(r"\b(address|addr)\s*[:\-]?\s*(.+)", re.IGNORECASE)
    aadhar_match = re.search(aadhar_number_pattern, text)
    if not aadhar_match:
        aadhar_match = re.search(aadhar_number_pattern_no_space, text)

    aadhar_number = aadhar_match.group().replace(" ", "") if aadhar_match else None
    name_match = name_pattern.search(text)
    name = name_match.group() if name_match else None
    dob_match = dob_pattern.search(text)
    dob = dob_match.group() if dob_match else None
    address_match = address_pattern.search(text)
    address = address_match.group(2) if address_match else None
    if aadhar_number and len(aadhar_number) == 12 and verhoeff_checksum(aadhar_number) and name and dob:
        return "Valid Aadhar Card", aadhar_number, name, dob
    else:
        return "Invalid Aadhar Card", aadhar_number, name, dob


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/verify", methods=["POST"])
def verify_document():
    if "document" not in request.files:
        return "No file uploaded!", 400

    file = request.files["document"]
    if file.filename == "":
        return "No selected file!", 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)
    extracted_text, error = extract_text_from_file(filepath)
    if error:
        return error, 500
    print("Extracted Text:\n", extracted_text)
    result, aadhar_number, name, dob = validate_aadhar_card(extracted_text)
    print(f"Validation Details:\nAadhar Number: {aadhar_number}\nName: {name}\nDOB: {dob}")

    return render_template(
        "index.html",
        result=result,
        aadhar_number=aadhar_number,
        name=name,
        dob=dob,
    )

if __name__ == "__main__":
    app.run(debug=True)

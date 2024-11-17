# CodeCrusaders

### **Project Description**

This AI-driven platform is designed to streamline access to government schemes and services, making it easier for individuals to discover, understand, and avail of the benefits of various government programs. The platform leverages Artificial Intelligence to verify documents, automate the discovery of eligible schemes based on personal profiles, and provide personalized guidance throughout the application process. By simplifying the process of finding relevant government schemes and offering tailored assistance, the platform empowers citizens to access their rightful benefits efficiently. It is built to enhance the user experience, ensuring that individuals can navigate government services with ease and clarity. The solution is inspired by the comprehensive listing of government schemes available on [MyScheme](https://www.myscheme.gov.in/).

### For Aadhaar verifier application:-

To run this project, you need to install the following dependencies: **Flask** for building the web application (`pip install Flask`), **pdf2image** to convert PDF files into images (`pip install pdf2image`), **Pillow** (PIL Fork) for image manipulation (`pip install Pillow`), **easyocr** for Optical Character Recognition (OCR) to extract text from images (`pip install easyocr`), **NumPy** for numerical computations (`pip install numpy`), and **OpenCV** for computer vision tasks (`pip install opencv-python`). If you're on Windows, you'll also need to install **Poppler** for `pdf2image`. To install all the required libraries, you can run `pip install -r requirements.txt` after cloning the repository.

### Milestones Achieved

- Developed an **Aadhaar Verifier Website** that validates the authenticity of Aadhaar cards, helping to detect fraudulent uploads. If the Aadhaar card is verified as genuine, the data extracted from it can be securely stored in a database. This data is then utilized to suggest personalized government schemes based on the individual's details, enhancing the user experience and streamlining the process of accessing relevant benefits.

  ### Eligibility Checker Application:

To run this *Eligibility Checker* project, you need to install the following dependencies:  
- *Flask* for building the web application (pip install Flask)  
- *Pandas* for data manipulation (pip install pandas)  
- *NumPy* for numerical computations (pip install numpy)  
- *Matplotlib* for data visualization (pip install matplotlib)  
- *Scikit-learn* for machine learning models (pip install scikit-learn)  
- *Pymongo* for interacting with MongoDB (pip install pymongo)  
- *JSON* for parsing JSON files (pip install json)

You can install all the required libraries by running the following command after cloning the repository:

bash
pip install -r requirements.txt


### Milestones Achieved:
I have developed an *Eligibility Checker Script* that evaluates a user's eligibility for various government schemes based on their profile data. This application utilizes machine learning models to predict and recommend relevant schemes by comparing user data with pre-loaded scheme criteria. Users can fill out a form, submit their details, and the system will return the schemes they qualify for.

### Steps to Use the Eligibility Checker:

1. *Set Up MongoDB*:  
   Create two databases on your local MongoDB instance:  
   - *schemeDB: This database will contain a collection named **schemes* with details of the available government schemes.  
   - *userDB: This database will contain a collection named **users* for storing user details.

2. *Import JSON Data*:  
   Import the *schemes* and *users* data into the respective collections in MongoDB. You can either manually input data or use a script to import data from a JSON file.

3. *Clone the Repository*:  
   Clone the repository containing the files:
   - check.py
   - eligibility_checker.py
   - index.html
   
4. *Set Up the Project Directory*:  
   Create a root directory, and inside this directory, place:
   - check.py
   - eligibility_checker.py  
   - A templates folder that contains the index.html file.

5. *Run the Application*:  
   Execute the following command to start the script:
   
   bash
   python check.py
   

6. *Fill Out the Form*:  
   Once the server is running, navigate to the provided URL, and fill out the user form. The form will collect details like age, income, and other criteria to check eligibility.

7. *View the Results*:  
   After submitting the form, the system will process the data and display the schemes you are eligible for based on your profile.

This *Eligibility Checker* provides a user-friendly way to streamline access to government schemes, making it easier for individuals to discover and apply for benefits they are qualified for.

### Features We are Working on

-

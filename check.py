from flask import Flask, render_template, request
import pymongo
from eligibility_checker import check_eligibility

app = Flask(__name__)

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
user_db = client["userDB"]  # Updated to userDB
scheme_db = client["schemeDB"]  # Updated to schemeDB
users_collection = user_db["users"]  # Updated to users collection
schemes_collection = scheme_db["schemes"]  # Updated to schemes collection

@app.route('/')
def index():
    return render_template('index.html', schemes=[], user=None)

@app.route('/submit', methods=['POST'])
def submit_form():
    user_data = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'age': int(request.form.get('age')),
        'gender': request.form.get('gender'),
        'location': request.form.get('location'),
        'occupation': request.form.get('occupation'),
        'disability_status': request.form.get('disability_status'),
        'caste': request.form.get('caste'),
        'income': int(request.form.get('income'))
    }

    # Call the eligibility checker function
    eligible_schemes = check_eligibility(user_data)

    # Debugging: Print the eligible schemes to the console
    print("Eligible Schemes:", eligible_schemes)

    # Render template with schemes and user data
    return render_template('index.html', schemes=eligible_schemes, user=user_data)

if __name__ == '__main__':
    app.run(debug=True)

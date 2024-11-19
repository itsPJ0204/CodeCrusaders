from flask import Flask, render_template, request
import pymongo
from eligibility_checker import check_eligibility

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")
user_db = client["userDB"]
scheme_db = client["schemeDB"]
users_collection = user_db["users"]
schemes_collection = scheme_db["schemes"]

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

    eligible_schemes = check_eligibility(user_data)
    print("Eligible Schemes:", eligible_schemes)
    return render_template('index.html', schemes=eligible_schemes, user=user_data)

if __name__ == '__main__':
    app.run(debug=True)

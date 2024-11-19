import pymongo
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")
user_db = client["userDB"]
scheme_db = client["schemeDB"]

def check_eligibility(user_data):
    if isinstance(user_data, str):
        user = json.loads(user_data)
    else:
        user = user_data

    user_age = user.get('age', 0)
    user_income = user.get('income', 0)
    user_location = user.get('location', "Unknown")
    user_gender = user.get('gender', "Unknown")
    user_caste = user.get('caste', "Unknown")
    user_disability_status = user.get('disability_status', "Not specified")

    eligible_schemes = []

    schemes = scheme_db["schemes"].find()
    for scheme in schemes:
        criteria = scheme.get('eligibility_criteria', {})

        age_min = criteria.get('age_min', None)
        age_max = criteria.get('age_max', None)
        income_min = criteria.get('income_min', None)
        income_max = criteria.get('income_max', None)
        location = criteria.get('location', None)
        gender = criteria.get('gender', None)
        caste = criteria.get('caste', None)
        disability_status = criteria.get('disability_status', None)

        if (age_min is None or age_min == "Not specified" or user_age >= age_min) and \
           (age_max is None or age_max == "Not specified" or user_age <= age_max):
            if (income_min is None or income_min == "Not specified" or user_income >= income_min) and \
               (income_max is None or income_max == "Not specified" or user_income <= income_max):
                if caste is None or caste == "Not specified" or user_caste == caste or "All" in caste:
                    if location is None or location == "Not specified" or user_location in location or "All" in location:
                        if gender is None or gender == "Not specified" or user_gender == gender or "All" in gender:
                            if disability_status is None or disability_status == "Not specified" or user_disability_status == disability_status or "All" in disability_status:
                                eligible_schemes.append(scheme['name'])

    return eligible_schemes

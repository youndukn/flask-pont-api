import firebase_admin
from firebase_admin import db, credentials

from flask import Flask, request, jsonify

app = Flask(__name__)

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": 'FIREBASE_DATABASE_URL'})

@app.route('/add_company', methods=['POST'])
def add_company():
    company_name = request.json['company_name']
    keyword = request.json['keyword']

    ref = db.reference('/companies')
    company_ref = ref.child(company_name) # Using company name as the key
    company_ref.set({
        'name': company_name,
        'keyword': keyword
    })

    return jsonify({"status": "success"}), 200

@app.route('/get_companies', methods=['GET'])
def get_companies():
    ref = db.reference('/companies')
    companies = ref.get()

    # Optionally, you can transform the data into a list if needed
    companies_list = [{"name": key, **value} for key, value in companies.items()] if companies else []

    return jsonify({"companies": companies_list}), 200

if __name__ == '__main__':
    app.run(debug=True)

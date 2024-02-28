from flask import Flask, jsonify
from faker import Faker

app = Flask(__name__)
fake = Faker('en_IN')  

# Generate user data with custom domain
def generate_users(count):
    users = []
    for _ in range(count):
        user = {
            "name": fake.name(),
            "email": fake.user_name() + '@pythonapplication.com',  #Email domain
            "address": fake.address(),
            "phone_number": fake.phone_number()
        }
        users.append(user)
    return users

# Generate 1000 users
users_data = generate_users(1000)

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users_data)

if __name__ == '__main__':
    app.run(debug=True)

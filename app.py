"""Small apps to demonstrate endpoints with basic feature - CRUD in MongoDB"""
import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId, json_util

# Load environment variables from the .env file
load_dotenv()
app = Flask(__name__)

mongodb_connection_addr = os.environ.get("MONGODB_CONNECTION", "mongodb://localhost:27017/")
db_name = os.environ.get("DATABASE_NAME", "db_library")
if not db_name:
    raise ValueError("The DATABASE_NAME environment variable is not set or is empty.")

# Connect to MongoDB
print(f'Connect to {mongodb_connection_addr}...')
client = MongoClient(mongodb_connection_addr)

db = client[db_name]  # connect and use database
collection = db['books']  # use collections object


# Test API Health
@app.route('/check')
def hello():
    """Endpoint for check database connection"""
    try:
        # The `ping` method checks the health of the connection
        client.admin.command('ping')
        return jsonify({"message": "MongoDB connection is healthy."})
    except Exception as e:
        return jsonify(f"MongoDB connection error: {e}")

# Create
@app.route('/create', methods=['POST'])
def create():
    """Endpoint for insert data"""
    data = request.get_json()

    # Insert data into MongoDB
    result = collection.insert_one(data)

    return jsonify({"message": "Document created successfully", "id": str(result.inserted_id)})

# Read
@app.route('/read')
def read():
    """Endpoint for read data"""
    # Retrieve all documents from MongoDB
    # db.books.find()
    records = collection.find().sort("_id", -1)
    data = list(records)

    # Serialize BSON types using json_util
    json_data = json_util.dumps(data)
    return json_data

# Update
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    """Endpoint for update data"""
    data = request.get_json()
    print(f'Update for books _id : {id}')
    # Update data in MongoDB
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    print(result)
    if result.modified_count > 0:
        return jsonify({"message": "Document updated successfully"})
    else:
        return jsonify({"message": "Query Executed, No Document Updated"})

# Delete
@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    """Endpoint for delete data"""
    # Delete data from MongoDB
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Document deleted successfully"})
    else:
        return jsonify({"message": "Document not found"})

if __name__ == '__main__':
    app.run(debug=True)

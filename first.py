from flask import Flask, jsonify, request
from bson import ObjectId
import pymongo

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb+srv://raushan:Rau@cluster0.dqcvoon.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

# read user data
@app.route("/read", methods=["GET"])
def get_user_data():
    try:
        store = []
        for x in mycol.find():
            # Convert ObjectId to string representation
            x["_id"] = str(x["_id"])
            store.append(x)
        return jsonify(store)
    except Exception as e:
        return jsonify({"message": "Error in code: " + str(e)})

# create user
@app.route("/create", methods=["POST"])
def add_user_data():
    try:
        data = request.get_json()
        mycol.insert_one(data)
        return jsonify({"message" : "Data is added"})
    except Exception as e:
        return jsonify({"message": "Error in code: " + str(e)})

# update user data
@app.route("/update/<id>",  methods=["PATCH"])
def upadate_user_data(id):
    try:
        filter_criteria = {'_id': ObjectId(id)}
        data = request.get_json()
        update_data = {'$set': data}
        mycol.update_one(filter_criteria, update_data)
        return jsonify({"message": "User data updated successfully"})
    except Exception as e:
        return jsonify({"message": "Error in code: " + str(e)})

# delete user data
@app.route("/delete/<id>", methods=["DELETE"])
def delete_user_data(id):
    try:
        filter_criteria = {'_id': ObjectId(id)}
        result = mycol.delete_one(filter_criteria)

        if result.deleted_count > 0:
            return jsonify({"message": "User data deleted successfully"})
        else:
            return jsonify({"message": "User data not found"})
    except Exception as e:
        return jsonify({"message": "Error in code: " + str(e)})

if __name__ == '__main__':
    app.run()

from datetime import datetime
from flask import jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://skyler:H1tB6ghk7bARsaqd@imhof-db.mm8br5c.mongodb.net/?retryWrites=true&w=majority&appName=IMHOF-DB"
client = MongoClient(uri, server_api=ServerApi('1'))

def get_info(code):
    try:
        # Access the database and collection
        collection = client.get_database("imhof").get_collection("data")

        # Aggregation pipeline to get all relevant records sorted by timestamp
        pipeline = [
            {"$match": {"code": code}},
            {"$sort": {"time": 1}}  # Sort by time in ascending order
        ]

        # Fetch the data
        data = list(collection.aggregate(pipeline))

        if not data:
            return {"current": 0, "lifetime": 0}

        lifetime_seconds = 0
        most_recent_status = data[-1]["oven_on"]
        now = datetime.utcnow()

        last_on_time = None
        for i in range(len(data)):
            if data[i]["oven_on"]:
                if last_on_time is None:
                    last_on_time = data[i]["time"]
            else:
                if last_on_time:
                    time_diff = (data[i]["time"] - last_on_time).total_seconds()
                    lifetime_seconds += time_diff
                    last_on_time = None

        if last_on_time:
            lifetime_seconds += (now - last_on_time).total_seconds()

        # Calculate current "on" duration since the last "off"
        current_seconds = 0
        for i in range(len(data) - 1, -1, -1):
            if not data[i]["oven_on"]:
                break
            current_seconds = (now - data[i]["time"]).total_seconds()

        return jsonify({
            "current": current_seconds,
            "lifetime": lifetime_seconds
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def set_oven_status(code, key, oven_on_status):
    try:
        # Access the database and collections
        db = client.get_database("imhof")
        auth_collection = db.get_collection("auth")
        data_collection = db.get_collection("data")

        # Check if there is a matching auth entry
        auth_check = auth_collection.find_one({"code": code, "key": key})

        # If no auth entry exists, check if there are any data records for the code
        if not auth_check:
            data_check = data_collection.find_one({"code": code})
            if not data_check:
                print("No existing data records found for code. Adding new auth entry.")
                auth_collection.insert_one({"code": code, "key": key})
            else:
                print("Authorization failed: Invalid code or key.")
                return 403

        # Create a new document with the current timestamp and oven status
        new_record = {
            "code": code,
            "time": datetime.utcnow(),
            "oven_on": oven_on_status
        }

        # Insert the new record into the data collection
        result = data_collection.insert_one(new_record)

        if result.acknowledged:
            print(f"Record inserted with id: {result.inserted_id}")
            return 200
        else:
            print("Failed to insert the record.")
            return 400

    except Exception as e:
        print(f"An error occurred: {e}")
        return 400


if __name__ == "__main__":
    # set_oven_status("1234", "foobar", True)
    print(get_info("1234"))
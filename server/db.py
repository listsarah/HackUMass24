from datetime import datetime

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
            {"$sort": {"time": 1}},  # Sort by time in ascending order
            {
                "$project": {
                    "time": 1,
                    "oven_on": 1,
                    "next_timestamp": {"$arrayElemAt": ["$timestamp", 1]}
                }
            }
        ]

        # Fetch the data
        data = list(collection.aggregate(pipeline))

        if not data:
            return {"current": 0, "lifetime": 0}

        lifetime_seconds = 0
        most_recent_status = data[-1]["oven_on"]
        now = datetime.utcnow()

        # Iterate through data to calculate the duration when the oven was 'on'
        for i in range(len(data) - 1):
            if data[i]["oven_on"]:
                time_diff = (data[i + 1]["time"] - data[i]["time"]).total_seconds()
                lifetime_seconds += time_diff

        # Add the time from the most recent record to now if it is 'on'
        if most_recent_status:
            time_diff = (now - data[-1]["time"]).total_seconds()
            lifetime_seconds += time_diff

        # Calculate the time difference from the most recent 'on' status to now
        current_seconds = (now - data[-1]["time"]).total_seconds() if most_recent_status else 0

        return {
            "current": current_seconds,
            "lifetime": lifetime_seconds
        }

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

        if not auth_check:
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
import json
import subprocess


def get_existing_subdomains():
    try:
        result = subprocess.run(
            ["gcloud", "dns", "record-sets", "list", "--zone=ismyhouseonfire-dev-zone", "--format=json"],
            capture_output=True, text=True, check=True
        )

        records = json.loads(result.stdout)
        max_index = 0

        for record in records:
            name = record.get("name", "")
            if name.startswith("api") and name.endswith(".ismyhouseonfire.dev."):
                try:
                    index = int(name[3:-21])  # Extract the number between "api" and ".ismyhouseonfire.dev."
                    max_index = max(max_index, index)
                except ValueError:
                    continue

        print(json.dumps({"next_api_index": max_index + 1}))
    except subprocess.CalledProcessError:
        # If there's an error fetching the DNS records, default to 1
        print("Error")
        print(json.dumps({"next_api_index": 1}))


if __name__ == "__main__":
    get_existing_subdomains()

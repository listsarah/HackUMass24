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
            if name.startswith("api") and name.endswith(".ismyhouseonfire.tech."):
                try:
                    index = int(name[3:-22])  # Extract the number between "api" and ".ismyhouseonfire.tech."
                    max_index = max(max_index, index)
                except ValueError:
                    continue

        return max_index + 1
    except subprocess.CalledProcessError:
        return 1

if __name__ == "__main__":
    # Wrap the output in a JSON object with string keys and values
    next_api_index = get_existing_subdomains()
    print(json.dumps({"next_api_index": str(next_api_index)}))

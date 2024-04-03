import base64
import json
with open('rock-star-tools-25g0k7-firebase-adminsdk-4hauj-c04cba05a0.json', "r") as file:
    json_data = json.load(file)
    json_string = json.dumps(json_data)

    base64_encoded = base64.b64encode(json_string.encode()).decode()
    print(base64_encoded)
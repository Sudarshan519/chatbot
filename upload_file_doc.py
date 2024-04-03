import base64
from datetime import datetime, timedelta
import json
import os
import shutil
import tempfile

from fastapi import File, HTTPException, UploadFile
import requests

from ai_tools_app.core. config import settings
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase Admin SDK
cred = credentials.Certificate(json.loads(base64.b64decode(os.environ.get('FIREBASE_CONFIG')).decode()))
firebase_admin.initialize_app(cred, {
    'storageBucket': 'rock-star-tools-25g0k7.appspot.com'
})

# def read_config():
#     with open("google-services.json") as config_file:
#         return json.load(config_file)

# config = read_config()
FIREBASE_STORAGE_BUCKET = "rock-star-tools-25g0k7.appspot.com"#config["FIREBASE_STORAGE_BUCKET"]
FIREBASE_API_KEY = "AIzaSyD4R8PD1XH6L3Ea7wvdqKE2jtk_RhmlNYw"#config["FIREBASE_API_KEY"]

async def upload_image(image: UploadFile = File(...)):
    try:
        # Read the contents of the uploaded file
        file_content = await image.read()

        # Create a storage client
        bucket = storage.bucket()

        # Upload the file contents to Firebase Storage
        destination_path = "images/" + image.filename
        blob = bucket.blob(destination_path)
        blob.upload_from_string(file_content)
        # Make the blob publicly accessible
        blob.make_public()
 
        # Generate the public URL for the uploaded file
        url = blob.public_url

        return {"image_url": url}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
# @app.get("/download/{filename}")
async def download_file(filename: str):
    # Create a storage client
        bucket = storage.bucket()

        # Upload the file contents to Firebase Storage
        destination_path = "images/" + filename
        blob = bucket.blob(destination_path)

    # Generate a signed URL that expires in 7 days
        expiry_period = timedelta(days=7)
        signed_url = blob.generate_signed_url(expiration=expiry_period)    
        return signed_url
    # url = f"{FIREBASE_STORAGE_BUCKET}/images/{filename}"
    # headers = {
    #     "Authorization": f"Bearer {FIREBASE_API_KEY}",
    # }
    # response = requests.get(url, headers=headers)
    # if response.status_code == 200:
    #     return response.content
    # else:
    #     raise HTTPException(status_code=response.status_code, detail=response.text)
    




def upload_image_to_firebase(image_path, destination_path):
    # Create a storage client
    bucket = storage.bucket()

    # Upload image
    blob = bucket.blob(destination_path)
    blob.upload_from_filename(image_path)
    
    # Generate download URL
    url = blob.public_url

    return url
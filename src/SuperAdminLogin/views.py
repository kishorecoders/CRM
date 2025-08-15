from fastapi import APIRouter, HTTPException, Header,Body,UploadFile, File, Depends, Request
from .service import UserService,show_all_count
from src.database import get_db
from sqlmodel import Session
from datetime import datetime
import boto3
from src.parameter import get_token
import os
import base64
from io import BytesIO
from typing import List

router = APIRouter()

@router.post("/login")
async def login(email: str = Body(...), password: str = Body(...), auth_token: str = Header(..., convert_underscores=True, alias="AuthToken")):
    response = UserService.login(auth_token, email, password)
    return response

@router.get("/DeshbordCount")
def read_all_deshbord_count_details(auth_token: str = Header(None, convert_underscores=True, alias="AuthToken"),db: Session = Depends(get_db)):
       def inner_get_plan(auth_token: str):
            if auth_token != get_token():
               return {"status": "false", "message": "Unauthorized Request"}
            else:
                return show_all_count(db=db)
    
       return inner_get_plan(auth_token)

@router.post("/user_profile_image")
def upload_user_profile_image(image: UploadFile = File(...)):

    image_path = upload_to_s3(image.file, "bucket-apl", f"uploads/images_{image.filename}")
    
    return {"image_url": image_path}

def upload_to_s3(file, bucket_name, key):
    
    aws_access_key_id = 'AKIA4IXGKBATOI6ZPM35'
    aws_secret_access_key = '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'
    
    aws_region = 'eu-north-1'

    
    s3 = boto3.client('s3', region_name=aws_region, aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    
    s3.upload_fileobj(file, bucket_name, key)
    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
    return s3_url

# @router.post("/upload-image/")
# async def upload_image(base64_image: str):
#     try:
#         # Decode base64 image string
#         image_data = base64.b64decode(base64_image)
        
#         current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

#         # Save the image to the 'uploads' folder
#         image_path = os.path.join("uploads", f"{current_datetime}.png")
#         with open(image_path, "wb") as image_file:
#             image_file.write(image_data)

#         # Get the URL of the saved image
#         image_url = f"/uploads/{current_datetime}.png"

#         return {"image_url": image_url}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


    
# @router.post("/upload-image/")
# async def upload_image(image: UploadFile = File(...)):
#     try:
#         # Get today's datetime as a string
#         current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

#         # Save the image to the 'uploads' folder with today's datetime as filename
#         image_path = os.path.join("uploads", f"{current_datetime}_{image.filename}")
#         with open(image_path, "wb") as image_file:
#             image_file.write(image.file.read())

#         # Get the URL of the saved image
#         image_url = f"https://api.entraguru.in/uploads/{current_datetime}_{image.filename}"

#         return {"image_url": image_url}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/upload-image/")
# async def upload_image(image: UploadFile = File(...)):
#     try:
#         # Create the 'uploads' folder if it doesn't exist
#         if not os.path.exists("uploads"):
#             os.makedirs("uploads")

#         # Get today's datetime as a string
#         current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

#         # Save the image to the 'uploads' folder with today's datetime as filename
#         image_path = os.path.join("uploads", f"{current_datetime}_{image.filename}")
#         with open(image_path, "wb") as image_file:
#             image_file.write(image.file.read())

#         # Get the URL of the saved image
#         image_url = f"http://localhost:8080/uploads/{current_datetime}_{image.filename}"

#         return {"image_url": image_url}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/upload-images/")
# async def upload_images(images: List[UploadFile] = File(...)):
#     try:
#         if not os.path.exists("uploads"):
#             os.makedirs("uploads")

#         image_urls = []

#         for image in images:
#             current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
#             image_path = os.path.join("uploads", f"{current_datetime}_{image.filename}")

#             with open(image_path, "wb") as image_file:
#                 image_file.write(image.file.read())

#             image_url = f"https://api.entraguru.in/uploads/{current_datetime}_{image.filename}"
#             image_urls.append(image_url)

#         return {"image_urls": image_urls}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/upload-images/")
# async def upload_images(request: Request, images: List[UploadFile] = File(...)):
#     try:
#         base_url = str(request.base_url)
#         if not os.path.exists("uploads"):
#             os.makedirs("uploads")

#         image_urls = []

#         for image in images:
#             current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
#             image_path = os.path.join("uploads", f"{current_datetime}_{image.filename}")

#             with open(image_path, "wb") as image_file:
#                 image_file.write(image.file.read())

#             image_url = f"{base_url}uploads/{current_datetime}_{image.filename}"
#             image_urls.append(image_url)

#         return {"image_urls": image_urls}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



MAX_FILE_SIZE_MB = 10  # Maximum file size allowed in MB for all files

@router.post("/upload-images/")
async def upload_images(request: Request, images: List[UploadFile] = File(...)):
    try:
        base_url = str(request.base_url)
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        image_urls = []

        for image in images:
            file_data = await image.read()



          # Check if the file size exceeds the limit
            file_size_mb = len(file_data) / (1024 * 1024)  # Convert to MB
            if file_size_mb > MAX_FILE_SIZE_MB:
                raise HTTPException(status_code=200, detail=f"File {image.filename} is too large. Maximum size is {MAX_FILE_SIZE_MB}MB.")

            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
            image_path = os.path.join("uploads", f"{current_datetime}_{image.filename}")

            # with open(image_path, "wb") as image_file:
            #     image_file.write(image.file.read())
            with open(image_path, "wb") as image_file:
                image_file.write(file_data)  # Use previously read data

            image_url = f"{base_url}/uploads/{current_datetime}_{image.filename}"
            image_urls.append(image_url)

        
        response_image_urls = [url.replace(str(request.base_url), "") for url in image_urls]

        return {"status": "true","image_urls": response_image_urls}
    except HTTPException as e:
        # Custom error response
        return {"status": "false", "message": f"{e.detail}"}
    except Exception as e:
        # General error handling
        return {"status": "false", "message": str(e)}


# @router.post("/upload-images/")
# async def upload_images(request: Request, images: List[UploadFile] = File(...)):
#     try:
#         base_url = str(request.base_url)
#         if not os.path.exists("uploads"):
#             os.makedirs("uploads")

#         image_urls = []

#         for image in images:
#             current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
#             image_path = os.path.join("uploads", f"{current_datetime}_{image.filename}")

#             with open(image_path, "wb") as image_file:
#                 image_file.write(image.file.read())

#             image_url = f"{base_url}/uploads/{current_datetime}_{image.filename}"
#             image_urls.append(image_url)

        
#         response_image_urls = [url.replace(str(request.base_url), "") for url in image_urls]

#         return {"image_urls": response_image_urls}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


from fastapi import APIRouter, HTTPException, UploadFile, status
from models.OCRModel import OCRModel, Base64PostModel
from models.RestfulModel import RestfulModel
from paddleocr import PaddleOCR
from utils.ImageHelper import base64_to_ndarray, bytes_to_ndarray
import requests
from PIL import Image
import numpy as np

# OCR_LANGUAGE = os.environ.get("OCR_LANGUAGE", "en")
router = APIRouter(prefix="/ocr", tags=["OCR"])
ocr = PaddleOCR(use_angle_cls=True, lang='en')

@router.get('/predict-by-path', response_model=RestfulModel, summary="Recognize Local Image")
def predict_by_path(image_path: str):
    result = ocr.ocr(image_path, cls=True)
    restfulModel = RestfulModel(
        resultcode=200, message="Success", data=result, cls=OCRModel)
    return restfulModel

@router.post('/predict-by-base64', response_model=RestfulModel, summary="Recognize Base64 Data")
def predict_by_base64(base64model: Base64PostModel):
    img = base64_to_ndarray(base64model.base64_str)
    result = ocr.ocr(img=img, cls=True)
    restfulModel = RestfulModel(
        resultcode=200, message="Success", data=result, cls=OCRModel)
    return restfulModel

@router.post('/predict-by-file', response_model=RestfulModel, summary="Recognize Uploaded File")
async def predict_by_file(file: UploadFile):
    restfulModel: RestfulModel = RestfulModel()
    if file.filename.endswith((".jpg", ".png")):
        restfulModel.resultcode = 200
        restfulModel.message = file.filename
        img = np.array(Image.open(file.file))
        # file_bytes = file_data.read()
        # img = bytes_to_ndarray(file_bytes)
        result = ocr.ocr(img=img, cls=True)
        restfulModel.data = result
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please upload a .jpg or .png format image"
        )
    return restfulModel

@router.get('/predict-by-url', response_model=RestfulModel, summary="Recognize Image URL")
async def predict_by_url(imageUrl: str):
    restfulModel: RestfulModel = RestfulModel()
    response = requests.get(imageUrl)
    image_bytes = response.content
    if image_bytes.startswith(b"\xff\xd8\xff") or image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        restfulModel.resultcode = 200
        img = bytes_to_ndarray(image_bytes)
        result = ocr.ocr(img=img, cls=True)
        restfulModel.data = result
        restfulModel.message = "Success"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please upload a .jpg or .png format image"
        )
    return restfulModel

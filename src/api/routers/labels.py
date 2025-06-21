import logging
from logging import getLogger
import json
import sys

from fastapi import APIRouter, UploadFile, Response, status

import api.flows as flows 
import api.models as models

logger = getLogger(__name__)
logger.setLevel("DEBUG")


router = APIRouter()


@router.post("/build_labels/", response_model=models.BuildLabelsResponse, status_code=200)
async def build_labels(file: UploadFile, config: UploadFile, response: Response):
    content = await file.read()
    config = await config.read()
    config = config.decode('utf-8')
    config = json.loads(config)

    logger.info(f"Received file: {file.filename}, size: {len(content)} bytes")
    if not content:
        logger.error("File is empty.")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return models.BuildLabelsResponse(errors=["El archivo está vacío."])
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):	
        logger.error("File must be a CSV or Excel file.")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return models.BuildLabelsResponse(errors=["El archivo debe ser un CSV o un archivo de Excel."]) 
    
    if file.filename.endswith('.csv'):
        logger.warning("Processing CSV file. Format may not be handled correctly")

    # df = func(BytesIO(content))
    builder = flows.BuildLabels(config)
    labels = builder.run(data=content, file_path=file.filename)
    return labels
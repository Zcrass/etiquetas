from io import BytesIO
import logging
from logging import getLogger
import json
import sys

from fastapi import APIRouter, UploadFile, File, Response, status
from fastapi.responses import JSONResponse
import pandas as pd

import api.flows as flows 
import api.models as models

logger = getLogger(__name__)
logger.setLevel("DEBUG")
if not logger.hasHandlers():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

router = APIRouter()


@router.post("/build_labels/", response_model=models.BuildLabelsResponse, status_code=200)
async def build_labels(file: UploadFile, config: UploadFile, response: Response):
    content = await file.read()
    config = await config.read()
    config = config.decode('utf-8')
    config = json.loads(config)

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
        # logger.warning("Advertencia: El archivo es un CSV, puede que no se procese correctamente si tiene encabezados o formatos especiales.")
        func = pd.read_csv
    else:
        func = pd.read_excel
    df = func(BytesIO(content))
    builder = flows.BuildLabels(config)
    labels = builder.run(data=df)
    return labels
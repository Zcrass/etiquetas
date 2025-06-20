from io import BytesIO
from logging import getLogger

from fastapi import APIRouter, UploadFile, File, Response, status
from fastapi.responses import JSONResponse
import pandas as pd

import api.flows as flows 
import api.models as models

logger = getLogger(__name__)
router = APIRouter()


@router.post("/build_labels/", response_model=models.BuildLabelsResponse, status_code=200)
async def build_labels(file: UploadFile, response: Response):
    content = await file.read()
    
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
    builder = flows.BuildLabels()
    labels = builder.run(data=df)
    return labels
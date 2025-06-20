from io import BytesIO
from logging import getLogger

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
import pandas as pd

from api.flows import BuildLabels

logger = getLogger(__name__)
router = APIRouter()


@router.post("/build_labels/")
async def build_labels(file: UploadFile = File(...)):
    content = await file.read()
    
    if not content:
        logger.error("File is empty.")
        return JSONResponse(status_code=400, content={"message": "El archivo está vacío o corrupto."})
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):	
        logger.error("File must be a CSV or Excel file.")
        return JSONResponse(status_code=400, content={"message": "El archivo debe ser un archivo CSV o Excel."})
    
    if file.filename.endswith('.csv'):
        logger.warning("Processing CSV file. Format may not be handled correctly")
        # logger.warning("Advertencia: El archivo es un CSV, puede que no se procese correctamente si tiene encabezados o formatos especiales.")
        func = pd.read_csv
    else:
        func = pd.read_excel
    df = func(BytesIO(content))
    builder = BuildLabels()
    labels = builder.run(data=df)
    return JSONResponse(labels)
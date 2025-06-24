import logging
from logging import getLogger
import json
import sys

from fastapi import APIRouter, UploadFile, Response, Form

import api.flows as flows 
import api.models as models

logger = getLogger(__name__)
logger.setLevel("DEBUG")


router = APIRouter()


@router.post("/build_labels/", response_model=models.BuildLabelsResponse, status_code=200)
async def build_labels(
    file: UploadFile, 
    template: UploadFile, 
    response: Response,
    columna_n_duplicados: str = Form("DUPLICADOS"),
    grid_template: UploadFile | None = None,
    ):

    try:
        logger.info(f"Duplicate column name {columna_n_duplicados}")
        logger.info(f"Received file: {file.filename}, size: {file.size} bytes")
        content = await file.read()
        template = await template.read()
        
        if grid_template is None:
            logger.info("Reading default grid template")
            with open("label_grid.html", "r", encoding="utf8") as file:
                grid_template = file.read()
        else:
            logger.info(f"Reading grid template from file {grid_template.filename}")
            grid_template = await grid_template.read()
            
        builder = flows.BuildLabels(columna_n_duplicados, grid_template)
        labels = builder.run(data=content, template=template)
    except Exception as exc:
        logger.error(f"Error during processing: {exc}")
        response.status_code = 500
        return models.BuildLabelsResponse(labels=None, errors=[str(exc)])
    return labels
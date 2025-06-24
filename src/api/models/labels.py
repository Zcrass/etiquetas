__all__ = [
    "BuildLabelsResponse",
]
from fastapi import UploadFile
from pydantic import BaseModel


class BuildLabelsResponse(BaseModel):
    """
    Response model for build labels.
    """
    labels: str | None = None
    """"HTML content of the labels, if generated successfully."""
    file: str | None = None
    """File path of the generated labels, if applicable."""
    errors: list[str] = []
    """List of error messages, if any occurred during processing."""




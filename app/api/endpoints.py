from fastapi import APIRouter, Depends, HTTPException, status, responses
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import RedirectResponse

from .. import crud, schemas
from ..database import SessionLocal
from ..utils import generate_shortcode

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )
    finally:
        db.close()


@router.post("/shorten", response_model=schemas.URLResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(request: schemas.URLCreate, db: Session = Depends(get_db)):
    original_url_str = str(request.url)
    existing_url = crud.get_url_by_original_url(db, original_url_str)

    if existing_url:
        location = f"/urls/{existing_url.shortcode}"
        return responses.Response(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": location})

    shortcode = generate_shortcode()
    while crud.get_url_by_shortcode(db, shortcode) is not None:
        shortcode = generate_shortcode()

    try:
        url = crud.create_short_url(db, original_url=original_url_str, shortcode=shortcode)
        response_data = schemas.URLResponse(
            shortcode=url.shortcode,
            url=url.original_url,
            created_on=url.created_on
        )
        headers = {"Location": f"/urls/{url.shortcode}"}
        return responses.JSONResponse(content=jsonable_encoder(response_data.model_dump()),
                                      status_code=status.HTTP_201_CREATED, headers=headers)
    except SQLAlchemyError as e:
        logger.error(f"Error creating short URL: {e}")
        raise HTTPException(status_code=500, detail="Error creating short URL")


@router.get("/urls/{shortcode}", response_class=RedirectResponse, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
def redirect_to_original(shortcode: str, db: Session = Depends(get_db)):
    try:
        url_data = crud.get_url_by_shortcode(db, shortcode)
        if url_data:
            return RedirectResponse(url=url_data.original_url)
        raise HTTPException(status_code=404, detail="Short Code not found")
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/urls/{shortcode}/stats", response_model=schemas.URLStats)
def get_statistics(shortcode: str, db: Session = Depends(get_db)):
    try:
        url_data = crud.get_url_stats(db, shortcode)
        if url_data:
            return schemas.URLStats(
                hits=url_data.hits,
                url=url_data.original_url,
                created_on=url_data.created_on
            )
        raise HTTPException(status_code=404, detail="URL not found")
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

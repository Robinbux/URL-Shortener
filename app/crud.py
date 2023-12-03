from sqlalchemy.orm import Session
from . import models


def get_url(db: Session, url_id: int):
    return db.query(models.URL).filter(models.URL.id == url_id).first()


def create_short_url(db: Session, original_url: str, shortcode: str):
    db_url = models.URL(original_url=original_url, shortcode=shortcode)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_url_by_shortcode(db: Session, shortcode: str):
    db_url = db.query(models.URL).filter(models.URL.shortcode == shortcode).first()
    if db_url:
        db_url.hits += 1
        db.commit()
        db.refresh(db_url)
    return db_url

def get_url_by_original_url(db: Session, original_url: str):
    db_url = db.query(models.URL).filter(models.URL.original_url == original_url).first()
    if db_url:
        db_url.hits += 1
        db.commit()
        db.refresh(db_url)
    return db_url

def get_url_stats(db: Session, shortcode: str):
    return db.query(models.URL).filter(models.URL.shortcode == shortcode).first()

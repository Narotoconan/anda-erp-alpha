from app.core.database import db_first_connection


def startup():
    db_first_connection()


__all__ = ['startup']

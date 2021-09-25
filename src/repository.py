from datetime import datetime
from db import engine
from sqlmodel import Session, select
session = Session(bind=engine)
from models import Birthday
from typing import List
from datetime import datetime

def create_birthday(bd: List):
    for i in bd:
        bd = Birthday(**i)
        session.add(bd)
    session.commit()


def get_all_birthdays_the_month(today:datetime):
    statement = select(Birthday).where(Birthday.month == today.month)
    results = session.exec(statement).all()
    return results

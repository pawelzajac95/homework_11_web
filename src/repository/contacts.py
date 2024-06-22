from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
from src.database.models import Contact
from src.schemas import ContactCreate

async def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

async def get_contacts(db: Session, search_query: str = None):
    if search_query:
        return db.query(Contact).filter(or_(
            Contact.first_name.ilike(f"%{search_query}%"),
            Contact.last_name.ilike(f"%{search_query}%"),
            Contact.email.ilike(f"%{search_query}%")
        )).all()
    else:
        return db.query(Contact).all()

async def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(first_name=contact.first_name, last_name=contact.last_name, email=contact.email, phone_number=contact.phone_number, birth_date=contact.birth_date)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

async def update_contact(db: Session, contact_id: int, contact: ContactCreate):
    db_contact = await get_contact(db, contact_id)
    if not db_contact:
        return None
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

async def delete_contact(db: Session, contact_id: int):
    db_contact = await get_contact(db, contact_id)
    if not db_contact:
        return None
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted successfully"}

async def get_contacts_upcoming_birthdays(db: Session):
    today = datetime.today().date()
    end_date = today + timedelta(days=7)
    return db.query(Contact).filter(
        (Contact.birth_date >= today) & (Contact.birth_date <= end_date)
    ).all()

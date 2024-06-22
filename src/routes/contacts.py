from fastapi import APIRouter, Query, FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.schemas import ContactCreate, Contact
from src.database.db import get_db
from src.repository.contacts import get_contact, create_contact, update_contact, delete_contact, get_contacts_upcoming_birthdays
from typing import List, Optional
from src.database import models
from src import database
from datetime import date, timedelta


models.Base.metadata.create_all(bind=database.db.engine)

app = FastAPI()
router = APIRouter(prefix='/contacts')
@router.post("/contacts/", response_model=Contact, status_code=status.HTTP_201_CREATED)
async def create_new_contact(contact: ContactCreate, db_session: Session = Depends(get_db)):
    return await create_contact(db_session, contact)

@router.get("/contacts/", response_model=List[Contact])
async def read_contacts(
    skip: int = 0,
    limit: int = 10,
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Contact)

    if first_name:
        query = query.filter(models.Contact.first_name.contains(first_name))
    if last_name:
        query = query.filter(models.Contact.last_name.contains(last_name))
    if email:
        query = query.filter(models.Contact.email.contains(email))

    contacts = query.offset(skip).limit(limit).all()
    return contacts

@router.get("/contacts/{contact_id}", response_model=Contact)
async def read_contact(contact_id: int, db_session: Session = Depends(get_db)):
    contact = await get_contact(db_session, contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.put("/contacts/{contact_id}", response_model=Contact)
async def update_existing_contact(contact_id: int, contact: ContactCreate, db_session: Session = Depends(get_db)):
    updated_contact = await update_contact(db_session, contact_id, contact)
    if not updated_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return updated_contact

@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_contact(contact_id: int, db_session: Session = Depends(get_db)):
    deleted = await delete_contact(db_session, contact_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return {"message": "Contact deleted successfully"}

@router.get("/contacts/upcoming_birthdays/", response_model=List[Contact])
def read_upcoming_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    upcoming = today + timedelta(days=7)
    query = db.query(models.Contact).filter(
        models.Contact.birth_date >= today,
        models.Contact.birth_date <= upcoming
    )
    contacts = query.all()
    return contacts
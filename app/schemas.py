from pydantic import BaseModel
from typing import Optional, List

class Item(BaseModel):
    name: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None

class DocumentData(BaseModel):
    document_type: Optional[str] = None
    language: Optional[str] = None
    document_title: Optional[str] = None
    date: Optional[str] = None
    document_number: Optional[str] = None
    person_name: Optional[str] = None
    organization_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    items: Optional[List[Item]] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    raw_text: Optional[str] = None
    confidence: Optional[float] = None

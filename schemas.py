from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime, date
import enum

class University(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        populate_by_name = True

class ApplicationStatus(enum.Enum):
    open = 'open'
    pending = 'pending'
    approved = 'approved'
    denied = 'denied'
    completed = 'completed'
    prospective_scholarship = 'prospective_scholarship'
    retroactive_scholarship = 'retroactive_scholarship'

class Application(BaseModel):
    id: int
    startTime: Optional[datetime] = Field(alias='date_applied')
    email: Optional[str] = None
    basicInformation_email: Optional[str] = Field(alias='email2')
    basicInformation_firstname: Optional[str] = Field(alias='first_name')
    basicInformation_lastname: Optional[str] = Field(alias='last_name')
    basicInformation_mobile: Optional[str] = Field(alias='phone_number')
    academicInformation_studentID: Optional[str] = Field(alias='mat_number')
    academicInformation_school: Optional[str] = Field(alias='university_string')
    basicInformation_countryofresidence: Optional[str] = Field(alias='country')
    basicInformation_regionofresidence: Optional[str] = Field(alias='region')
    basicInformation_address: Optional[str] = Field(alias='address')
    academicInformation_graduation: Optional[datetime] = Field(alias='graduation_date')
    university: Optional[University] = None
    status: Optional[ApplicationStatus] = None
    start_date: Optional[datetime] = None
    tuition_amount: Optional[float] = None
    arrears_amount: Optional[float] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True

class Applications(BaseModel):
    results: List[Application]
    total: int

class Finances(BaseModel):
    application_fee: Optional[float] = None
    total_advances: Optional[float] = None
    total_membership_fees: Optional[float] = None
    total_deposited: Optional[float] = None
    total_expected: Optional[float] = None
    total_remaining: Optional[float] = None

class ApplicationResolve(BaseModel):
    approve: bool
    university_id: Optional[int] = None
    start_date: Optional[date] = None
    tuition_amount: Optional[float] = None
    arrears_amount: Optional[float] = None

    @validator('university_id', 'start_date', 'tuition_amount', 'arrears_amount', pre=True, always=True)
    def check_approved_fields(cls, v, values, **kwargs):
        if 'approve' in values and not values['approve']:
            return None
        if v is None:
            raise ValueError(f"{kwargs['field'].name} must not be None when approved")
        return v
    
class ApplicationCreate(BaseModel):
    email: Optional[str] = Field(...)
    basicInformation_firstname: str = Field(alias='first_name')
    basicInformation_lastname: str = Field(alias='last_name')
    basicInformation_mobile: Optional[str] = Field(alias='phone_number')
    academicInformation_studentID: str = Field(alias='mat_number')
    basicInformation_countryofresidence: Optional[str] = Field(alias='country')
    basicInformation_regionofresidence: Optional[str] = Field(alias='region')
    basicInformation_address: Optional[str] = Field(alias='address')
    tuition_amount: Optional[float] = Field(...)
    arrears_amount: Optional[float] = Field(...)
    start_date: Optional[date] = Field(...)
    status: ApplicationStatus = Field(...)
    academicInformation_graduation: Optional[date] = Field(alias='graduation_date')
    university_id: int = Field(alias='university')

class ApplicationUpdate(BaseModel):
    email: Optional[str] = Field(...)
    basicInformation_firstname: Optional[str] = Field(alias='first_name')
    basicInformation_lastname: Optional[str] = Field(alias='last_name')
    basicInformation_mobile: Optional[str] = Field(alias='phone_number')
    academicInformation_studentID: Optional[str] = Field(alias='mat_number')
    basicInformation_countryofresidence: Optional[str] = Field(alias='country')
    basicInformation_regionofresidence: Optional[str] = Field(alias='region')
    basicInformation_address: Optional[str] = Field(alias='address')
    tuition_amount: Optional[float] = Field(...)
    arrears_amount: Optional[float] = Field(...)
    start_date: Optional[date] = Field(...)
    status: Optional[ApplicationStatus] = Field(...)
    academicInformation_graduation: Optional[date] = Field(alias='graduation_date')
    university_id: Optional[int] = Field(alias='university')

class DepositStudent(BaseModel):
    id: int
    basicInformation_firstname: str = Field(alias='first_name')
    basicInformation_lastname: str = Field(alias='last_name')

    class Config:
        from_attributes = True
        populate_by_name = True

class Deposit(BaseModel):
    id: int
    date: datetime
    memo: str
    amount: float
    student: Optional[DepositStudent]
    reference_id: Optional[str]

    class Config:
        from_attributes = True
        populate_by_name = True

class Deposits(BaseModel):
    results: List[Deposit]
    total: int

class DepositCreate(BaseModel):
    date: date
    memo: str
    amount: float
    reference_id: Optional[str] = None

class DepositCreateSingle(BaseModel):
    student_id: int
    date: date
    memo: str
    amount: float
    reference_id: Optional[str] = None

class DepositResolve(BaseModel):
    student_mat: str

class DepositUpdate(BaseModel):
    date: date
    memo: str
    amount: float
    reference_id: Optional[str] = None

class InvoiceType(enum.Enum):
    advance = 'advance'
    membership_fee = 'membership_fee'
    application_fee = 'application_fee'
    other = 'other'

class Invoice(BaseModel):
    id: int
    created_at: datetime
    memo: Optional[str] = None
    amount: Optional[float] = None
    student_id: int
    type: InvoiceType

    class Config:
        from_attributes = True
        populate_by_name = True

class Invoices(BaseModel):
    results: List[Invoice]
    total: int

class InvoiceUpdate(BaseModel):
    memo: str
    amount: float
    type: InvoiceType

class InvoiceCreateSingle(BaseModel):
    student_id: int
    memo: str
    amount: float
    type: InvoiceType

class Comment(BaseModel):
    id: int
    student_id: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class CommentCreate(BaseModel):
    student_id: int
    message: str

class CommentUpdate(BaseModel):
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    admin_id: int
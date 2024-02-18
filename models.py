from sqlalchemy import BigInteger, Column, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, Enum, TIMESTAMP, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text
from schemas import InvoiceType, ApplicationStatus

Base = declarative_base()

class SequelizeMeta(Base):
    __tablename__ = 'SequelizeMeta'

    name = Column(String(255, 'utf8_unicode_ci'), primary_key=True, unique=True)

class University(Base):
    __tablename__ = 'universities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    app_fee_flat = Column(Float)
    app_fee_percentage = Column(Float)
    during_studies_min_payment = Column(Float)
    during_studies_membership_fee = Column(Float)
    after_studies_min_payment = Column(Float)
    after_studies_membership_fee = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))

class Application(Base):
    __tablename__ = 'application'

    __table_args__ = (
        Index('idx_fulltext_applications', 'email', 'basicInformation_firstname', 'basicInformation_lastname', 'basicInformation_address', 'basicInformation_countryofresidence', 'basicInformation_regionofresidence', 'academicInformation_studentID', mysql_prefix='FULLTEXT'),
    )

    id = Column(Integer, primary_key=True)
    jpfID = Column(String(50), unique=True)
    deviceID = Column(String(50))
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    location__ = Column(Text)
    email = Column(Text)
    review_authorize = Column(Text)
    basicInformation_firstname = Column(Text)
    basicInformation_lastname = Column(Text)
    basicInformation_TIN = Column(Text)
    basicInformation_dob = Column(DateTime)
    basicInformation_gender = Column(Text)
    basicInformation_cobirth = Column(Text)
    basicInformation_countryofbirth = Column(Text)
    basicInformation_address = Column(Text)
    basicInformation_coresidence = Column(Text)
    basicInformation_countryofresidence = Column(Text)
    basicInformation_regionofresidence = Column(Text)
    basicInformation_ethnicity = Column(Text)
    basicInformation_mobile = Column(Text)
    basicInformation_email = Column(Text)
    basicInformation_referral = Column(Text)
    academicInformation_highested = Column(Text)
    academicInformation_school = Column(Text)
    academicInformation_major = Column(Text)
    academicInformation_secondMajor = Column(Text)
    academicInformation_workStatus = Column(Text)
    academicInformation_status = Column(Text)
    academicInformation_studentID = Column(Text)
    academicInformation_currentgpa = Column(Text)
    academicInformation_graduation = Column(DateTime)
    academicInformation_intended = Column(Text)
    academicInformation_currentearnings = Column(Text)
    academicInformation_consistentearnings = Column(Text)
    academicInformation_postGraduation = Column(DateTime)
    phoneOwnership_provider = Column(Text)
    phoneOwnership_ownphone = Column(Text)
    phoneOwnership_buyphone = Column(Text)
    phoneOwnership_mobilePhone = Column(Text)
    phoneOwnership_howLong = Column(Text)
    loanSpecifics_willing_to_pay = Column(Float)
    loanSpecifics_loanSize = Column(Float)
    loanSpecifics_howSoon = Column(Text)
    loanSpecifics_firstLoan = Column(Text)
    loanSpecifics_whatDoLoan = Column(Text)
    loanSpecifics_appFee = Column(Float)
    loanSpecifics_arrears = Column(Text)
    loanSpecifics_semAmount = Column(Text)
    references_firstname1 = Column(Text)
    references_surname1 = Column(Text)
    references_title1 = Column(Text)
    references_organization1 = Column(Text)
    references_email1 = Column(Text)
    references_mobile1 = Column(Text)
    references_relationship1 = Column(Text)
    references_firstname2 = Column(Text)
    references_surname2 = Column(Text)
    references_title2 = Column(Text)
    references_organization2 = Column(Text)
    references_email2 = Column(Text)
    references_mobile2 = Column(Text)
    references_relationship2 = Column(Text)
    references_firstname3 = Column(Text)
    references_surname3 = Column(Text)
    references_title3 = Column(Text)
    references_organization3 = Column(Text)
    references_email3 = Column(Text)
    references_mobile3 = Column(Text)
    references_relationship3 = Column(Text)
    nationalIdentity = Column(String(50))
    studentID = Column(String(50))
    academicTranscript = Column(String(50))
    WASSCE = Column(String(50))
    employment = Column(String(50))
    isWhatsAppAllowed = Column(Integer)
    status = Column(Enum(ApplicationStatus), index=True)
    university_id = Column(ForeignKey('universities.id'), index=True)
    start_date = Column(DateTime)
    tuition_amount = Column(Float)
    arrears_amount = Column(Float)
    university = relationship('University')

class Deposit(Base):
    __tablename__ = 'deposits'
    
    __table_args__ = (
        Index('idx_fulltext_deposits', 'memo', 'student_name', 'student_email', 'student_mat', mysql_prefix='FULLTEXT'),
    )

    id = Column(Integer, primary_key=True)
    memo = Column(String(255))
    student_id = Column(ForeignKey('application.id'), index=True)
    amount = Column(Float)
    date = Column(DateTime)
    complete = Column(Boolean, nullable=False, default=True)
    reference_id = Column(String(255))
    student_name = Column(String(255))
    student_email = Column(String(255))
    student_mat = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    student = relationship('Application')

class Invoice(Base):
    __tablename__ = 'invoices'

    __table_args__ = (
        Index('idx_fulltext_invoices', 'memo', 'student_name', 'student_email', 'student_mat', mysql_prefix='FULLTEXT'),
    )

    id = Column(Integer, primary_key=True)
    memo = Column(String(255))
    student_id = Column(ForeignKey('application.id'), nullable=False, index=True)
    amount = Column(Float)
    type = Column(Enum(InvoiceType))
    student_name = Column(String(255))
    student_email = Column(String(255))
    student_mat = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    student = relationship('Application')

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    student_id = Column(ForeignKey('application.id'), nullable=False, index=True)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    student = relationship('Application')

class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
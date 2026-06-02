from pydantic import BaseModel, EmailStr


class EmailValidationRequest(BaseModel):
    email: EmailStr


class EmailValidationResponse(BaseModel):
    email: EmailStr
    is_valid: bool
    message: str

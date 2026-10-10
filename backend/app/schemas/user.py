from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    """
    Data the frontend sends when a new user signs up.
    """
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """
    Data the frontend sends when a user logs in.
    """
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Safe user data to send back to the frontend.
    Notice: no password field here — we never send that back.
    """
    id: str
    username: str
    email: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """
    What we send back after successful signup/login.
    """
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
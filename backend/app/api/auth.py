from fastapi import APIRouter, HTTPException

from app.schemas.user import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.services.user_repository import (
    find_user_by_email,
    create_user,
)


router = APIRouter()


@router.post("/signup", response_model=TokenResponse)
def signup(request: SignupRequest):
    existing_user = find_user_by_email(request.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists",
        )

    new_user = create_user(
        username=request.username,
        email=request.email,
        hashed_password=hash_password(request.password),
    )

    token = create_access_token({"sub": new_user["id"]})

    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=new_user["id"],
            username=new_user["username"],
            email=new_user["email"],
        ),
    )


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    user = find_user_by_email(request.email)

    if not user or not verify_password(
        request.password,
        user["hashed_password"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    token = create_access_token({"sub": user["id"]})

    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user["id"],
            username=user["username"],
            email=user["email"],
        ),
    )
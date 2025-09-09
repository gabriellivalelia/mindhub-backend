from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.user import User
from app.core.security import hash_password

app = FastAPI()

@app.post("/create_user")
async def create_user(email: str, password: str, db: AsyncSession = Depends(get_db)):
    new_user = User(email=email, hashed_password=hash_password(password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"id": str(new_user.id), "email": new_user.email}

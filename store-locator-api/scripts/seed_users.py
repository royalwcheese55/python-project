from app.db.database import SessionLocal
from app.models.user import User
from app.auth.security import hash_password

def run():
    db = SessionLocal()
    users = [
        ("U001", "admin@test.com", "admin"),
        ("U002", "marketer@test.com", "marketer"),
        ("U003", "viewer@test.com", "viewer"),
    ]

    for uid, email, role in users:
        if not db.query(User).filter(User.email == email).first():
            db.add(User(
                user_id=uid,
                email=email,
                password_hash=hash_password("TestPassword123!"),
                role=role,
                status="active",
            ))
    db.commit()
    db.close()
    print("Seeded users")

if __name__ == "__main__":
    run()
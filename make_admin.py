from app import app, db
from models import User

with app.app_context():
    username = "Yaroslav"
    # пароль: 123
    user = User.query.filter_by(username=username).first()

    if user:
        user.is_admin = True
        db.session.commit()
        print(f"{user.username} is now an admin")
    else:
        print("User not found")
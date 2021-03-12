from uuid import uuid4
import datetime
import jwt
from flask import current_app
from selfInstall import db


class User(db.Model):
    # class to define users and store Email, unique id and public id

    __tablename__ = "siteUser"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    # maybe use PID here for tools
    # using this random string to encode JWT
    publicId = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))

    def __repr__(self):
        return (
            f"<User email={self.email}, public id={self.publicId}, admin={self.admin}>"
        )

    @classmethod
    def findByEmail(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def findByPublicId(cls, publicId):
        return cls.query.filter_by(publicId=publicId).first()

    def encodeAccessToken(self):
        now = datetime.datetime.utcnow()
        # payload = dict(exp=expire, iat=now, sub=self.public_id, admin=self.admin)
        # adding the exp= to this payload will make the JWT tokens have an experation date
        payload = dict(iat=now, sub=self.publicId, admin=self.admin)
        key = current_app.config.get("SECRET_KEY")
        return jwt.encode(payload, key, algorithm="HS256")

    @staticmethod
    def decodeAccessToken(accessToken):
        if isinstance(accessToken, bytes):
            accessToken = accessToken.decode("ascii")
        if accessToken.startswith("Bearer "):
            split = accessToken.split("Bearer")
            accessToken = split[1].strip()
        try:
            key = current_app.config.get("SECRET_KEY")
            payload = jwt.decode(accessToken, key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            error = "Access token expired"
            return error
        except jwt.InvalidTokenError:
            error = "Invalid token"
            return error

        userDict = dict(
            public_id=payload["sub"],
            admin=payload["admin"],
            token=accessToken,
        )
        return userDict

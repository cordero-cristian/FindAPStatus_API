from flask_restx import Model
from flask_restx.fields import String, Boolean
from flask_restx.inputs import email
from flask_restx.reqparse import RequestParser


authReqparser = RequestParser(bundle_errors=True)
authReqparser.add_argument(
    name="email", type=email(), location="form", required=True, nullable=False
)
authReqparser.add_argument(
    name="admin", type=bool, location="form", required=False, nullable=False
)
acccessPointModel = Model(
    "Access Point MAC",
    {
        "email": String,
        "admin": Boolean,
        "public_id": String,
    },
)

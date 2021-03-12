from flask_restx import Model
from flask_restx.fields import String, Boolean
from flask_restx.inputs import regex
from flask_restx.reqparse import RequestParser


accessPointStatusReqParser = RequestParser(bundle_errors=True)
accessPointStatusReqParser.add_argument(
    name="mac", type=regex('([0-9A-Fa-f]{2}(:)){5}([0-9A-Fa-f]{2})'), location="headers", required=True, nullable=False
)

user_model = Model(
    "mac",
    {
        'Controller': String,
        'ControllerIp': String,
        'IpAddress': String,
        'Location': String,
        'Model': String,
        'Name': String,
        'operationState': String,
        'radioMac': String,
        'radioOperStatus': String,
        'radioSlot': String,
        'radioStatus': String,
        'radioTxPower': String,
    },
)

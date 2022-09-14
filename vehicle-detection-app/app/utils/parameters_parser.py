from marshmallow import Schema, fields
import json

class AppParameters(Schema):
    car_cascade_src = fields.Str()
    bus_cascade_src = fields.Str()
    full_filename = fields.Str()
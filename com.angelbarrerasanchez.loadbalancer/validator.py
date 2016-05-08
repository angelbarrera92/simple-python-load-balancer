from jsonschema import validate
import jsonschema, sys

user_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "pattern": "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"},
        "password": {"type": "string", "minLength": 6, "maxLength": 30},
    },
    "required": ["email", "password"]
}

app_machine_schema = {
    "type": "object",
    "properties": {
        "host": {"type": "string"},
        "port": {"type": "number", "minimum": 0, "maximum": 65535},
    },
    "required": ["host", "port"]
}


def is_user_json_valid(user_json):
    try:
        validate(user_json,user_schema)
        return True
    except jsonschema.exceptions.ValidationError as ve:
        #sys.stderr.write("Record #{}: ERROR\n".format(user_json))
        sys.stderr.write(str(ve) + "\n")
        return False


def is_machine_json_valid(machine_json):
    try:
        validate(machine_json, app_machine_schema)
        return True
    except jsonschema.exceptions.ValidationError as ve:
        # sys.stderr.write("Record #{}: ERROR\n".format(user_json))
        sys.stderr.write(str(ve) + "\n")
        return False
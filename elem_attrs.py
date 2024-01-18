attributes = {
    "_id": "id",
    "className": "class",
    "style": "style",
    "src": "src",
    "value": "value",
    "placeholder": "placeholder",
    "alt": "alt"
}

variables = {
    "id": "id",
    "className": "class",
    "style": "style",
    "src": "src",
    "value": "value",
    "placeholder": "placeholder",
    "alt": "alt"
}

def getreverse(attr):
    for i, j in variables.items():
        if j==attr:
            return i
    return None
from document import Document, HTMLElement
import json

def parseEvents(document: Document, data):
    data = json.loads(data)
    if data["_id"] not in document.socket_messages:
        document.socket_messages.append(data["_id"])
        el:HTMLElement = document.querySelector("#" + data["elementId"])
        if(data["type"] == "click"):
            if(el.onClick != None):
                el.onClick(el)

        if(data['type'] == "change"):
            if "value" in data:
                el.value = data['value']
                el._changed = True
            return el, "focus"

    return None
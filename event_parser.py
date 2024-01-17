from document import Document, HTMLElement
import json

def parseEvents(document: Document, data):
    data = json.loads(data)
    el:HTMLElement = document.querySelector("#" + data["elementId"])
    if(data["type"] == "click"):
        if(el.onClick != None):
            el.onClick(el)

    if(data['type'] == "change"):
        el.value = data['value']
        el._changed = True
        return el, "focus"

    return None
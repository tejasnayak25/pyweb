const socket = new WebSocket("wss://" + location.host + "/websocket?path="+location.pathname);  // Use the WebSocket port

function func() {
    return ( ( ( 1+Math.random() ) * 0x10000 ) | 0 ).toString( 16 ).substring( 1 );
}

const randomUuid = () => {
    const UUID = (func() + func() + "-" + func() + "-3" + func().substring(0,2) + "-" + func() + "-" + func() + func() + func()).toLowerCase();
    return UUID;
};

socket.addEventListener("open", (event) => {
    console.log("WebSocket connection opened:", event);
    Listeners();
});

socket.addEventListener("error", (event) => {
    console.log(event);
});

socket.addEventListener("message", (event) => {
    if(event.data !== "") {
        let data = JSON.parse(event.data);
        let changes = data.changes;

        Object.keys(changes).forEach(key => {
            if(key === "document") {
                document.documentElement.innerHTML = changes[key];
            } else {
                let el = document.querySelector(`#${key}`);
                el.outerHTML = changes[key];
            }
        });

        if(data.id) {
            let el = document.querySelector("#"+data.id);
            if(data.effect === "focus") {
                const end = el.value.length;

                el.setSelectionRange(end, end);
                el.focus();
            }
        }
        Listeners();
    }
});

socket.addEventListener("close", (event) => {
    console.log("WebSocket connection closed:", event);
});

function sendEventData(eventType, elementId, value = "") {
    let eventData = {
        _id: randomUuid(),
        type: eventType,
        elementId: elementId,
    };

    if(value !== "") {
        eventData.value = value;
    }

    socket.send(JSON.stringify(eventData));
}

function eventHandler(event, element) {
    if(event.type === "change" && (element.nodeName.toLowerCase() === "input" || element.nodeName.toLowerCase() === "textarea")) {
        sendEventData(event.type, event.target.id || 'no-id', element.value || "");
    } else {
        sendEventData(event.type, event.target.id || 'no-id');
    }
}

function Listeners() {
    let events = ['click', 'dblclick', 'change', 'cancel', 'contextmenu', 'copy', 'cut', 'paste', 'pause', 'play']
    for (var key of events) {
        const eventType = key;

        eval(`
            document.querySelector("#main").on${eventType} = (event) => {
                const targetElement = event.target;
                const eventType = event.type;

                // Check if the clicked element is an input or textarea and the event is a click
                if ((targetElement.nodeName.toLowerCase() === 'input' || targetElement.nodeName.toLowerCase() === 'textarea') && eventType === 'click') {
                    return;
                }

                eventHandler(event, targetElement);
            };
        `);
    }

}
// Example: Send a message to the server
function sendMessage() {
    const message = prompt("Enter your message:");
    socket.send(message);
}
const socket = new WebSocket("wss://localhost:10000/websocket?path="+location.pathname);  // Use the WebSocket port

socket.addEventListener("open", (event) => {
    console.log("WebSocket connection opened:", event);
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
        listeners();
    }
});

socket.addEventListener("close", (event) => {
    console.log("WebSocket connection closed:", event);
});

function sendEventData(eventType, elementId, value) {
    let eventData = {
        type: eventType,
        elementId: elementId,
    };

    if(value) {
        eventData.value = value;
    }

    socket.send(JSON.stringify(eventData));
}

listeners();

function listeners() {
    document.querySelector("#main").querySelectorAll('button').forEach(element => {
        element.addEventListener('click', function(event) {
            sendEventData('click', element.id || 'no-id');
        });
    });

    document.querySelector("#main").querySelectorAll('input').forEach(element => {
        element.addEventListener("change", function(event) {
            sendEventData('change', element.id || 'no-id', element.value);
        });

        // element.addEventListener('keydown', function(event) {
        //     sendEventData('keydown', element.id || 'no-id');
        // });
    });
}
// Example: Send a message to the server
function sendMessage() {
    const message = prompt("Enter your message:");
    socket.send(message);
}

$(function() {
    var ws = new WebSocket('ws://localhost:8000/ws_v1/public/');
    ws.onmessage = function(e) {
        console.log(e);
    }
});

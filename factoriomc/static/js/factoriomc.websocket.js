"use strict"

FactorioMC.WebSocket = {
  socket: null,
  connected: false,
  reconnect_tries: 0,
  queue: [],
  connection_indicator: undefined,
  queue_status: undefined,
  init: function(endpoint) {
    m(m.INFO, "Initializing Websocket..");
    if (endpoint) {
      this.endpoint = endpoint;
      this.connect();
    } else {
      m(m.INFO, "No endpoint..");
    }
    this.connection_indicator = $("#connectionindicator");
    this.queue_status = $('#queue_status');
  },
  connect: function() {
    var url = WEBSOCKET_BASEURL + this.endpoint;
    m(m.INFO, "Opening connection to: "+url);

    this.socket = new WebSocket(url);
    this.reconnect_tries++;

    var me = this;
    this.socket.onopen = function() {
      m(m.INFO, "Connected.");
      me.connected = true;
      me.connection_indicator.hide();
      me.queue_status.hide();
      me.reconnect_tries = 0;

      me.flush_queue();
    }
    this.socket.onclose = function() {
      m(m.ERROR, "Disconnected..");
      me.connection_indicator.show();
      me.queue_status.show();
      me.connected = false;
      var delay = me.reconnect_tries;
      if (delay > 10) {
        delay = 10;
      }
      m(m.DEBUG, "Retrying connection in "+ delay +" seconds.");
      window.setTimeout(function() { me.connect() }, 1000 * delay);
    }
    this.socket.onmessage = function(e) {
      m(m.DEBUG, "Message received: "+e.data);
      var payload = JSON.parse(e.data);
      var event = new CustomEvent(payload['namespace'] + '::' + payload['status'],
          { 'detail': payload['data'] });
      window.dispatchEvent(event);
    }
  },
  flush_queue: function() {
    m(m.DEBUG, "Queue holds " + this.queue.length + " message(s)..");
    if (this.queue.length > 0) {
      m(m.DEBUG, "Sending them..");
      // Loop over the queue once. If the socket would disconnect while we are flushing
      // the queue, we don't want to get stuck here..
      for (var i=0; i<=this.queue.length; i++) {
        this.__send(this.queue.pop());
      }
    }
  },
  send: function(namespace, data) {
    var payload = {
      "namespace": namespace,
      "data": data
    };
    if (!this.connected) {
      m(m.ERROR, "Trying to send a message while not connected... Queing it.");
      this.queue.push(payload);
      this.queue_status.text(this.queue.length)
      return false;
    }
    this.__send(payload);

    return true;
  },
  __send: function(payload) {
    var payload_json = JSON.stringify(payload);
    m(m.DEBUG, "Sending: " + payload_json)
    this.socket.send(payload_json);
  }
}

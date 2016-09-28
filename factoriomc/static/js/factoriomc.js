"use strict"

var FactorioMC = {
  socket: undefined,

  Settings: {
      DEBUG: true,
      DEBUG_LOG_LEVEL: 0
    },

  init: function(endpoint) {
      this.socket = FactorioMC.WebSocket;
      this.socket.init(endpoint);
    }
}
function m(loglevel) {
  if (FactorioMC.Settings.DEBUG) {
      var prepend = 'UNDEFINED';
      switch(loglevel) {
            case m.DEBUG:
              prepend = 'DEBUG';
              break;
            case m.INFO:
              prepend = 'INFO';
              break;
            case m.WARNING:
              prepend = 'WARNING';
              break;
            case m.ERROR:
              prepend = 'ERROR';
              break;

          }
      var log_at = typeof FactorioMC.Settings.DEBUG_LOG_LEVEL !== 'undefined' ?
        FactorioMC.Settings.DEBUG_LOG_LEVEL : m.WARNING;

      var msg = Array.prototype.slice.call(arguments).slice(1, arguments.length).join(', ')
        if (loglevel >= log_at) {
                if (loglevel == m.DEBUG_NO_PREP) {
                          console.log(msg);
                        } else {
                          console.log(prepend + ": " + msg);
                        }
              }
    }
}
m.DEBUG_NO_PREP = 1;
m.DEBUG = 2;
m.INFO = 3;
m.WARNING = 4;
m.ERROR = 5;

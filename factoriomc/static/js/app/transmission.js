/**
 * Transmission js
 */

$(function() {

  var MIN_WAIT = 0.5,
    MAX_WAIT = 2,
    CHAR_DELAY = 200;

    var date = new Date();

    var transmission_str = [
        "Incoming transmission",
        "Date: "+date.toLocaleString()+" | Sender: a͡͞p̶t͘͟a ͏̢d̴̨̢er̢̧͠i̴̕v͡a",
        "  ",
        "We finally managed a secure channel.",
        "The newspapers have gone haywire lately. The colloseum the overlords were building has suddenly stopped; they're no longer responding.",
        "Stakeholders are outraged and the workers are starting to panic.",
        "...",
        "...",
        "Connection failed."
    ];



    var init_tramission = function(selector) {
        var transmission_block = $(selector);
        var waw = waitAndWrite.bind(transmission_block);

        writeArray(transmission_block, transmission_str)
    }

    var writeArray = function(entity, str_arr) {
        if (str_arr && str_arr.length > 0) {
            var waw = waitAndWrite.bind(entity);
            return Promise.resolve().then(function() {
                return waw(str_arr.shift(), random(2, 3));
            }).then(function() {
                writeArray(entity, str_arr)
            })
        }
    }

    // Time in secs
    var waitAndWrite = function(message, time) {
        if (message) {
            var entity = $('<div class="entry"></div>');
            this.append(entity);

            return new Promise(function(resolve, reject) {
                setTimeout(function() {
                    entity.append('> ');
                    entity.addClass('blink')

                    setTimeout(function() {
                        entity.removeClass('blink')
                        writer(entity, message, resolve)
                    }, time * 1000)
                }, CHAR_DELAY)

            });
        } else {
            return
        }
    }

    var writer = function(entity, str, cb) {
        if (str && str.length > 0) {
            var char = str.slice(0, 1);
            str = str.slice(1);
            setTimeout(function() {
                entity.append(char);
                writer(entity, str, cb)
            }, 70);
        } else {
            cb();
        }
    }

    var random = function(min, max) {
        return (Math.random() * (max - min) + min)
    }

    init_tramission('#main .transmission');

})

package.loaded.config = nil

config = require "config"

local led = {}

local pin = config.gpio

led.index = 0
led.pattern = {}
led.patternSize = 0;

tmr.register(2, 500, tmr.ALARM_SEMI, function() led.vibrate(led.pattern) end)

led.vibrate = function(pattern)
    led.patternSize = table.getn(led.pattern)
    state = led.pattern[led.index]

    if state == 0 then
        gpio.write(pin, gpio.HIGH)
    else
        gpio.write(pin, gpio.LOW)
    end
    if led.index < led.patternSize then
        led.index = led.index + 1
    else
        led.index = 0
    end
    tmr.start(2)
end

led.init = function()
    gpio.mode(pin, gpio.OUTPUT)
    gpio.write(pin, gpio.HIGH)
end

led.init()

led.on = function()
    tmr.start(2)
end

led.off = function()
    tmr.stop(2)
end

return led

package.loaded.config = nil
package.loaded.led = nil

config = require "config"
led = require "led"

local wsclient = {}

tmr.register(0, 1000, tmr.ALARM_SEMI, function() wsclient.setup() end)

connect = function(ws)
    ws:connect(config.host)
end

identify = function(ws)
    ws:send(config.secretID)
end

parsePayload = function(payload)
    if payload == nil then
        return
    end

    ok, data = pcall(cjson.decode, payload)

    if not ok then
        print("Failed decoding")
        return
    end

    if type(data["pattern"]) == "table" then
        led.pattern = data["pattern"]
    end
    
    if data["on"] == true then
        led.on()
    elseif data["on"] == false then
        led.off()
    end
        
end

registerCallbacks = function(ws)
    ws:on("connection", function(ws)
        print("connected")
        identify(ws)
    end)
    ws:on("receive", function(_, msg, opcode)
        print("payload received", opcode)
        parsePayload(msg)
    end)
    ws:on("close", function(_, status)
        print("disconnected", status)
        -- atempt reconnect
        tmr.start(0)
    end)
end

wsclient.setup = function()
    ws = websocket.createClient()
    registerCallbacks(ws)
    connect(ws)
end

return wsclient

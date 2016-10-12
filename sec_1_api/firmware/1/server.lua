package.loaded.led = nil
package.loaded.config = nil
led = require "led"
config = require "config"
local server = {}

server.createHTTPServer = function()
    if srv~=nil then
      srv:close()
    end

    srv = net.createServer(net.TCP)
    srv:listen(80, function(conn)
        conn:on("receive", function(sck, payload)
            if string.find(payload, "toggle") ~= nil then
                print("toggled")
                led.toggle()
            end
            sck:send("OK")
        end)
        conn:on("sent", function(sck) sck:close() end)
    end)
end

server.sendGet = function()
    sk = net.createConnection(net.TCP, 0)
    sk:on("receive", function(sck, payload)
        print(payload)
    end)

    sk:on("connection", function(sck,c)
        -- Wait for connection before sending.
        sck:send("GET / HTTP/1.1\r\nHost: 192.168.0.36\r\nConnection: keep-alive\r\nAccept: */*\r\n\r\n")
    end)
    sk:connect(config.port, config.host)
end

server.pollForCommands = function()
    tmr.alarm(0, 5000, 1, function()
        server.sendGet()
    end)
end

server.setupWifi = function()
    -- connect to WiFi access point
    wifi.setmode(wifi.STATION)
    wifi.sta.config(config.SSID, config.password)
    print(wifi.sta.getip())
end

return server

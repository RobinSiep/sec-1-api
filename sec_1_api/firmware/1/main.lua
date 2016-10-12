package.loaded.server = nil
package.loaded.led = nil
package.loaded.wsclient = nil
server = require "server"
led = require "led"
wsclient = require "wsclient"
led.init()
server.setupWifi()
wsclient.setup()



params = {red=0, green=0, blue=0, period=500, rpt=0}
ptimer = 0
power = false

pwm.setup(1, 500, 0) -- LED RED
pwm.setup(2, 500, 0) -- LED GREEN
pwm.setup(3, 500, 0) -- LED BLUE
pwm.start(1)
pwm.start(2)
pwm.start(3)

function split(str, pattern, n)
   if not string.find(str, pattern) then
      return { str }
   end
   local result = {}
   local fpat = "(.-)" .. pattern
   local insertCnt = 1
   local lastEnd = 1
   local s, e, cap = string.find(str, fpat, 1)
   while s do
      if insertCnt > n and n > 0 then
         break
      end
      if s ~= 1 or cap ~= "" then
         table.insert(result, cap)
      end
      insertCnt = insertCnt + 1
      lastEnd = e + 1
      s, e, cap = string.find(str, fpat, lastEnd)
   end
   if lastEnd <= #str then
      cap = string.sub(str, lastEnd)
      table.insert(result, cap)
   end
   return result
end

function pp()
   local k, v
   local s = ""
   for k,v in pairs(params) do s = s.."<br>\n"..k..":"..v end
   return s
end

function getparams(s)
   local t = split(s, "\n", 2) -- get first line
   t = split(t[1], " ", 4) -- get 'GET' argument
   -- t[1]: s = "/ctrl/?red=0&green=64&blue=255&period=500&rpt=300"
   t = split(t[2], "/", 2)
   if not (#t > 1 and t[1] == 'ctrl' and string.sub(t[2], 1, 1) == '?') then
      return false
   end
   tt = split(string.sub(t[2], 2), "&", 10)
   local k, v
   for k, v in pairs(tt) do
      local a = split(v, "=", 2)
      local k = a[1]
      local v = a[2]
      if params[k] ~= nil then
         v = tonumber(v)
         if v < 0 then v = 0 end
         if k ~= 'period' and k ~= 'rpt' and v > 1023 then v = 1023 end
         params[k] = v
      end
   end
   print(pp())
   tmfunc()

   return true
end

function led(r, g, b)
   print("R:"..r..",G:"..g..",B:"..b)
   pwm.setduty(1, r)
   pwm.setduty(2, g)
   pwm.setduty(3, b)
end

function tmfunc()
   local npower = power
   if params['rpt'] > 0 then
      if params['period'] == 0 then
         npower = true
      else
         if ptimer > 0 then
            ptimer = ptimer - 1
         else
            npower = not power
            if not npower then params['rpt'] = params['rpt'] - 1 end
            ptimer = params['period'] / 200
         end
      end
   else
      npower = off
   end

   -- LED on or off by params['power']
   if power ~= npower then
      power = npower
      if power then led(params['red'], params['green'], params['blue']) else led(0, 0, 0) end
   end
end

--

wifi.setmode(wifi.STATION)
wifi.sta.config("SSID", "PASSWORD")
wifi.sta.autoconnect(1)

tmr.register(0, 100, tmr.ALARM_AUTO, function() tmfunc() end)
tmr.start(0)

srv=net.createServer(net.TCP)
srv:listen(80,
           function(conn) 
              conn:on("receive",
                      function(conn,payload) 
                         print(payload)
                         local r = getparams(payload)
                         if r then
                            conn:send("<h1>ESP8266 - Signal NodeMCU working!</h1><p>"..pp().."</p>")
                         else
                            conn:send("<h1>ESP8266 - Server is working!</h1><p>"..pp().."</p>")
                         end
                         conn:close()
              end)
end)

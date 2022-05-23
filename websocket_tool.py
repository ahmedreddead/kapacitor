import ssl
import random
import websocket

home_assistant_ip = '192.168.0.100:8123'
home_assistant_access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI2Y2JlYTcxZTE0YTA0ZWRkYTcyMGY5MWIwNzk1YTQyOSIsImlhdCI6MTY1Mjc4ODI5NCwiZXhwIjoxOTY4MTQ4Mjk0fQ.y3TX9pJDZTmj50aK27dni3d-0oiNyOAyosvWcMURvGE'
#{"type":"supervisor/api","endpoint":"/addons/a0d7b954_influxdb/info","method":"get","id":25}

class home_assistant_websocket :
    def __init__(self, home_assistant_ip, home_assistant_access_token):
        self.home_assistant_ip = home_assistant_ip
        self.home_assistant_access_token = home_assistant_access_token
        self.message = '{"type": "auth","access_token":"' + home_assistant_access_token + '" }'
        self.api_name_influx = ''
        self.session = ''
        self.ws = ''
        self.auth_message = ''
        self.influx_long_id = ''

    def connect_home_Assistant(self) :
        #websocket.enableTrace(True)
        self.ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        self.ws.connect("wss://{}/api/websocket".format(self.home_assistant_ip))
        self.ws.recv()
        self.ws.send(self.message)
        self.auth_message = self.ws.recv()


    def get_influx_add_ones_name(self) :
        id = random.randrange(50, 500)
        self.ws.send('{"type":"supervisor/api","endpoint":"/addons","method":"get","id":'+str(id)+'}')
        dic = self.ws.recv()
        index = str(dic).find('{"name":"InfluxDB","slug":')
        slug = dic[index:index + 46]
        self.api_name_influx = str(slug).split(',')[1].split(':')[1].replace("\"", '')

    def get_influx_session (self) :
        id = random.randrange(500, 1000)
        self.ws.send('{"type":"supervisor/api","endpoint":"/ingress/session","method":"post","id":'+str(id)+'}')
        st = self.ws.recv()
        index = str(st).find('{"session":')
        st = st[index:]
        st = str(st).split(':')[1].replace('\"', '').replace("}", '')
        self.session = st

    def get_influx_long_id(self) :
        id = random.randrange(1000, 1500)
        self.ws.send('{"type":"supervisor/api","endpoint":"/addons/'+self.api_name_influx+'/info","method":"get","id":'+str(id)+'}')
        dic = self.ws.recv()
        index = str(dic).find('"ingress_url":')
        dic = dic[index:index+160]
        self.influx_long_id = str(dic).replace('\"','').split(',')[0].split(':')[1]

    def start(self):
        self.connect_home_Assistant()
        self.get_influx_add_ones_name()
        self.get_influx_session()
        self.get_influx_long_id()


object = home_assistant_websocket(home_assistant_ip , home_assistant_access_token)
object.start()
print(object.session ,object.influx_long_id)




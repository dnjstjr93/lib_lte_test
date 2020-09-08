import json, sys, serial
import paho.mqtt.client as mqtt

argv = sys.argv

my_lib_name = 'lib_sparrow_lte'

broker_address = 'localhost'

try:
    lib = dict()
    with open(my_lib_name + '.json', 'r') as f:
        lib = json.load(f)
        lib = json.loads(lib)

except:
    lib = dict()
    lib["name"] = my_lib_name
    lib["target"] = 'armv6'
    lib["description"] = "[name] [portnum] [baudrate]"
    lib["scripts"] = './' + my_lib_name + ' /dev/ttyUSB1 115200'
    lib["data"] = ['LTE']
    lib["control"] = []
    lib = json.dumps(lib, indent="\t")

    with open('./' + my_lib_name + '.json', 'w', encoding='utf-8') as make_file:
        json.dump(lib, make_file, indent="\t")


lib['serialPortNum'] = argv[1]
lib['serialBaudrate'] = argv[2]


# def on_connect(client,userdata,flags, rc):
#     if rc == 0:
#         print('[msw_mqtt_connect] connect to ', broker_address)
#     else:
#         print("Bad connection Returned code=", rc)


# def on_disconnect(client, userdata, flags, rc=0):
# 	print(str(rc))


# def on_publish(client, userdata, mid):
#     print("In on_pub callback mid= ", mid)


# def on_subscribe(client, userdata, mid, granted_qos):
#     print("subscribed: " + str(mid) + " " + str(granted_qos))


# def on_message(client, userdata, msg):
#     print(str(msg.payload.decode("utf-8")))



# client = mqtt.Client()

# client.on_connect = on_connect
# client.on_disconnect = on_disconnect
# client.on_subscribe = on_subscribe
# client.on_message = on_message

# client.connect(broker_address, 1883)

# client.subscribe('common', 1)
# client.loop_forever()


def missionPortOpening(missionPort, missionPortNum, missionBaudrate):
    if (missionPort == None):
        try:
            missionPort = serial.Serial(missionPortNum, missionBaudrate, timeout = 10)
            print ('missionPort open. ' + missionPortNum + ' Data rate: ' + missionBaudrate)
        except serial.SerialException as e:
            print ('lib serialport open error: ' + e)
    else:
        if (missionPort.is_open == False):
            missionPort.open()

            # lteQ.rssi = -Math.random()*100;
            # var container_name = 'LTE';
            # var data_topic = '/MUV/data/' + lib.name + '/' + container_name;

            # setTimeout(send_data_to_msw, 0, data_topic, lteQ);

missionPort = None
missionPortNum = lib["serialPortNum"]
missionBaudrate = lib["serialBaudrate"]
missionPortOpening(missionPort, missionPortNum, missionBaudrate)

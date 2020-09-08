import json, sys, serial, threading
import paho.mqtt.client as mqtt
from time import sleep

argv = sys.argv

my_lib_name = 'lib_sparrow_lte'

global lib_topic
broker_ip = 'localhost'
port = 1883
global lib_mqtt_client

global missionPort
lteQ = {}
sleep_sec = 1

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
#         print('[msw_mqtt_connect] connect to ', broker_ip)
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

# client.connect(broker_ip, 1883)

# client.subscribe('common', 1)
# client.loop_forever()


def missionPortOpening(missionPort, missionPortNum, missionBaudrate):
    if (missionPort == None):
        try:
            missionPort = serial.Serial(missionPortNum, missionBaudrate, timeout = 2)
            print ('missionPort open. ' + missionPortNum + ' Data rate: ' + missionBaudrate)
            mission_thread = threading.Thread(
                target=missionPortData, args=(missionPort,)
            )
            mission_thread.start()

            return missionPort

        except serial.SerialException as e:
            missionPortError(e)
        except TypeError as e:
            missionPortClose()
    else:
        if (missionPort.is_open == False):
            missionPortOpen()

def missionPortOpen():
    print('missionPort open!')
    missionPort.open()

def missionPortClose():
    global missionPort
    print('missionPort closed!')
    missionPort.close()


def missionPortError(err):
    print('[missionPort error]: ', err)


def lteReqGetRssi(missionPort):
    if missionPort is not None:
        if missionPort.is_open:
            atcmd = b'AT@DBG\r'
            missionPort.write(atcmd)

# def send_data_to_msw (data_topic, obj_data):
#     lib_mqtt_client.publish(data_topic, obj_data)


def missionPortData(missionPort):
    lteQ = dict()
    while True:
        lteReqGetRssi(missionPort)
        missionStr = missionPort.readlines()
        # print (arrRssi)

        arrLTEQ = missionStr[1].decode("utf-8").split(", ")
        for idx in range(len(arrLTEQ)):
            arrQValue = arrLTEQ[idx].split(':')
            if (arrQValue[0] == '@DBG'):
                lteQ['plmn'] = arrQValue[2]
            elif (arrQValue[0] == 'Band'):
                lteQ['band'] = int(arrQValue[1])
            elif (arrQValue[0] == 'EARFCN'):
                lteQ['earfcn'] = int(arrQValue[1])
            elif (arrQValue[0] == 'Bandwidth'):
                print('bandwidth origin: ', arrQValue[1])
                lteQ['bandwidth'] = int(arrQValue[1][:-3])
                print('bandwidth: ', lteQ['bandwidth'])
            elif (arrQValue[0] == 'PCI'):
                lteQ['pci'] = int(arrQValue[1])
            elif (arrQValue[0] == 'Cell-ID'):
                lteQ['cell_id'] = arrQValue[1]
            elif (arrQValue[0] == 'GUTI'):
                lteQ['guti'] = arrQValue[1]
            elif (arrQValue[0] == 'TAC'):
                lteQ['tac'] = int(arrQValue[1])
            elif (arrQValue[0] == 'RSRP'):
                print('rsrp origin: ', arrQValue[1])
                lteQ['rsrp'] = float(arrQValue[1][:-3])
                print('rsrp: ', lteQ['rsrp'])
            elif (arrQValue[0] == 'RSRQ'):
                print('rsrq origin: ', arrQValue[1])
                lteQ['rsrq'] = float(arrQValue[1][:-3])
                print('rsrq: ', lteQ['rsrq'])
            elif (arrQValue[0] == 'RSSI'):
                print('rssi origin: ', arrQValue[1])
                lteQ['rssi'] = float(arrQValue[1][:-3])
                print('rssi: ', lteQ['rssi'])
            elif (arrQValue[0] == 'SINR'):
                print('sinr origin: ', arrQValue[1])
                lteQ['sinr'] = float(arrQValue[1][:-2])
                print('sinr: ', lteQ['sinr'])




        # send_data_to_msw(data_topic,lteQ)

        # lteQ.rssi = -Math.random()*100;
        # var container_name = 'LTE';
        # var data_topic = '/MUV/data/' + lib.name + '/' + container_name;

        # setTimeout(send_data_to_msw, 0, data_topic, lteQ);

missionPort = None
missionPortNum = lib["serialPortNum"]
missionBaudrate = lib["serialBaudrate"]
missionPortOpening(missionPort, missionPortNum, missionBaudrate)

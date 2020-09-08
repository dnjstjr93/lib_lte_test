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
            missionPort = serial.Serial(missionPortNum, missionBaudrate, timeout = 10)
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
            missionPort.open()

def missionPortClose():
    global missionPort
    print('missionPort closed!')
    missionPort.close()


def missionPortError(err):
    print('[missionPort error]: ', err)


def lteReqGetRssi(missionPort):
    if missionPort is not None:
        if missionPort.isOpen():
            atcmd = b'AT@DBG\r'
            missionPort.write(atcmd)

# def send_data_to_msw (data_topic, obj_data):
#     lib_mqtt_client.publish(data_topic, obj_data)


def missionPortData(missionPort):
    while True:
        arrRssi = missionPort.read()
#        send_data_to_msw(data_topic,lteQ)

            # lteQ.rssi = -Math.random()*100;
            # var container_name = 'LTE';
            # var data_topic = '/MUV/data/' + lib.name + '/' + container_name;

            # setTimeout(send_data_to_msw, 0, data_topic, lteQ);

missionPort = None
missionPortNum = lib["serialPortNum"]
missionBaudrate = lib["serialBaudrate"]
missionPortOpening(missionPort, missionPortNum, missionBaudrate)


# def missionPortOpen(missionPortNum, missionBaudrate):
#     # Connect serial
#     global missionPort
#     print('Connect to serial...')
#     try:
#         missionPort = serial.Serial(missionPortNum, missionBaudrate, timeout=2)
#         if missionPort.isOpen():
#             print('missionPort Open. ', missionPortNum, 'Data rate: ', missionBaudrate)
#             mission_thread = threading.Thread(
#                 target=missionPortData, args=(missionPort,)
#             )
#             mission_thread.start()

#             return missionPort
#     except serial.SerialException as e:
#         missionPortError(e)
#     except TypeError as e:
#         missionPortClose()
#         missionPort.close()


# def missionPortClose():
#     print('missionPort closed!')


# def missionPortError(err):
#     print('[missionPort error]: ', err)


# def lteReqGetRssi(missionPort):
#     if missionPort is not None:
#         if missionPort.isOpen():
#             atcmd = b'AT@DBG\r'
#             missionPort.write(atcmd)


# def send_data_to_msw (data_topic, obj_data):
#     lib_mqtt_client.publish(data_topic, obj_data)


# def missionPortData(missionPort):
#     while True:
#         arrRssi = missionPort.read()
# #        send_data_to_msw(data_topic,lteQ)

# def msw_mqtt_connect(broker_ip, port):
#     lib_mqtt_client = mqtt.Client()
#     lib_mqtt_client.on_connect = on_connect
#     lib_mqtt_client.on_disconnect = on_disconnect
#     lib_mqtt_client.on_subscribe = on_subscribe
#     lib_mqtt_client.on_message = on_message
#     lib_mqtt_client.connect(broker_ip, port)
#     lib_muv_topic = '/MUV/control/'+ lib['name'] + '/MICRO'
#     lib_mqtt_client.subscribe(lib_muv_topic, 0)
#     print(lib_muv_topic)
# #    for idx in lib['topic']:
# #        if idx in lib['topic']:
# #            idx = lib['topic'].index(idx)
# #            lib_mqtt_client.subscribe(str(lib['topic'][idx]))
# #    print('[lib_mqtt_connect] lib_topic[' ,'+', idx ,'+' ']: ', lib['topic'][idx]);
#     lib_mqtt_client.loop_start()
#     # lib_mqtt_client.loop_forever()
#     return lib_mqtt_client


# def on_connect(client, userdata, flags, rc):
#     print('[msg_mqtt_connect] connect to ', broker_ip)


# def on_disconnect(client, userdata, flags, rc=0):
#     print(str(rc))


# def on_subscribe(client, userdata, mid, granted_qos):
#     print("subscribed: " + str(mid) + " " + str(granted_qos))


# def on_message(client, userdata, msg):
# #    for idx in lib['topic']:
# #        if idx in lib['topic']:
# #            idx = lib['topic'].index(idx)
# #            if msg.topic == lib['topic'][idx]:
#                 payload = msg.payload.decode('utf-8')
#                 on_receive_from_msw(msg.topic, str(payload))


# def on_receive_from_msw(topic, str_message):
#     print('[' + topic + '] ' + str_message)
# #    str_message = {"con":str_message}
#     cinObj = json.loads(str_message)
# #    print(cinObj)
#     request_to_mission(cinObj)


# def request_to_mission(cinObj):
#     if missionPort != None:
#         if missionPort.isOpen():
#             con = cinObj['con']
#             con_arr = con.split(',')
#             if (int(con_arr[0]) < 8) and (int(con_arr[1]) < 8):
#                 stx = 'A2'
#                 command = '030' + con_arr[0] + '0' + con_arr[1] + '000000000000'
#                 crc = 0
#                 print(command)
#                 for i in range(0,len(command),2):
#                     crc ^= int(command[i+1],16)
#                 if crc < 16:
#                     command += ('0' + str(crc))
#                 else :
#                     command += str(crc)

#                 etx = 'A3'
#                 command = stx + command + etx
#                 print('command: ', command)

#                 msdata = bytes.fromhex(command)
#                 print('msdata: ', msdata)
#                 missionPort.write(msdata)

# #lib={}
# def main():
#     global lib
#     argv = sys.argv[1:]  # argv 가져오기
#     if argv != None:
#         lib = {'name': argv[0], 'serialPortNum': argv[1], 'serialBaudrate': argv[2]}  # argv값 셋팅
#         print(lib)
#         # sys argv input
#         lib_mqtt_client = msw_mqtt_connect(broker_ip, port)
#         missionPort = missionPortOpen(lib['serialPortNum'], lib['serialBaudrate'])
# #        missionPort = missionPortOpen(missionPortNum, missionBaudrate)
#     else :
#         print("Input the argv!")

# #    lib_mqtt_client = msw_mqtt_connect(broker_ip, port)
# #    missionPort = missionPortOpen(missionPortNum, missionBaudrate)
# #    print(missionPort)

# if __name__ == "__main__":
#     main()
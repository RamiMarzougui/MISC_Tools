from canlib import canlib, Frame
import time
from random import randint
import cantools
import threading

############################# README ################################
# Fonction : Génère des trames aléatoires pour un réseau CAN
# Utilisation : 
#  - Envoie les datas via interface KVASER
#  - 3 interfaces PEAK sont branchées sur l'interface KVASER
#  - Un filtre (PCAN explorer)permet de répartir les trames
#    par interface PEAK
#####################################################################

#Send Id avec un cycle de 10ms
def send_can_dbc_100ms():
    while True:
        try:
            #génère data aléatoire pour chaque trame
            can_msg = None
            for el in list_100ms:
                list_data = [randint(0,255),randint(0,255),randint(0,255),
                            randint(0,255),randint(0,255),randint(0,255),
                            randint(0,255),randint(0,255)]
                if el["id"] == 452664324 or el["id"] == 452664320:
                    can_msg  = Frame(id_=el["id"], data=list_data, dlc = el["dlc"], flags=canlib.canMSG_EXT)
                else:
                    can_msg  = Frame(id_=el["id"], data=list_data, dlc = el["dlc"], flags=canlib.MessageFlag.STD )
                ch_a.write(can_msg)
        except Exception as e:
            print (e)
        time.sleep(0.1)

#Send Id avec un cycle de 100ms
def send_can_dbc_500ms():
    while True:
        try:
            #génère data aléatoire pour chaque trame
            for el in list_500ms:
                list_data = [randint(0,255),randint(0,255),randint(0,255),
                            randint(0,255),randint(0,255),randint(0,255),
                            randint(0,255),randint(0,255)]
                can_msg  = Frame(id_=el["id"], data=list_data, dlc = el["dlc"], flags=canlib.MessageFlag.STD )            
                ch_a.write(can_msg)
        except Exception as e:
            print (e)
        time.sleep(0.5)

#Send Id avec un cycle de 1000ms
def send_can_dbc_1000ms():
    while True:
        try:
            #génère data aléatoire pour chaque trame
            for el in list_1000ms:
                list_data = [randint(0,255),randint(0,255),randint(0,255),
                            randint(0,255),randint(0,255),randint(0,255),
                            randint(0,255),randint(0,255)]
                can_msg  = Frame(id_= el["id"], data=list_data, dlc = el["dlc"], flags=canlib.MessageFlag.STD )               
                ch_a.write(can_msg)
        except Exception as e:
            print (e)
        time.sleep(1)

#Envoi des datas sur le CAN2, id[0x501...0x50F]
def send_can2():
    # Liste des ids et dlc du can 2
    list_can_2 = [{'id_hex':'0x601','dlc':8},
                  {'id_hex':'0x602','dlc':7},
                  {'id_hex':'0x603','dlc':6},
                  {'id_hex':'0x604','dlc':5},
                  {'id_hex':'0x605','dlc':4},
                  {'id_hex':'0x606','dlc':3},
                  {'id_hex':'0x607','dlc':8},
                  {'id_hex':'0x608','dlc':8},
                  {'id_hex':'0x609','dlc':8},
                  {'id_hex':'0x60A','dlc':8},
                  {'id_hex':'0x60B','dlc':8},
                  {'id_hex':'0x60C','dlc':8},
                  {'id_hex':'0x60D','dlc':8},
                  {'id_hex':'0x60E','dlc':8},
                  {'id_hex':'0x60F','dlc':8}]
    while True:
        try:
            #génère data aléatoire pour chaque trame
            for msg in list_can_2:
                # COnversion id en decimal pour l'envoi su rle can
                id_dec = int(msg['id_hex'],16)
                # init list_data
                list_data = []
                for octet in range (0,msg["dlc"]):
                    octet = randint(0,255)
                    list_data.append(octet)
                can_msg  = Frame(id_= id_dec, data=list_data, dlc = msg["dlc"], flags=canlib.MessageFlag.STD )               
                ch_a.write(can_msg)
        except Exception as e:
            print (e)
            raise
        time.sleep(0.1)

def send_can3():
    # Liste des ids et dlc du can 2
    list_can_3 = [{'id_hex':'0x501','dlc':8},
                  {'id_hex':'0x502','dlc':7},
                  {'id_hex':'0x503','dlc':6},
                  {'id_hex':'0x504','dlc':5},
                  {'id_hex':'0x505','dlc':4},
                  {'id_hex':'0x506','dlc':3},
                  {'id_hex':'0x507','dlc':8},
                  {'id_hex':'0x508','dlc':8},
                  {'id_hex':'0x509','dlc':8},
                  {'id_hex':'0x50A','dlc':8},
                  {'id_hex':'0x50B','dlc':8},
                  {'id_hex':'0x50C','dlc':8},
                  {'id_hex':'0x50D','dlc':8},
                  {'id_hex':'0x50E','dlc':8},
                  {'id_hex':'0x50F','dlc':8}]
    while True:
        try:
            #génère data aléatoire pour chaque trame
            for msg in list_can_3:
                # COnversion id en decimal pour l'envoi su rle can
                id_dec = int(msg['id_hex'],16)
                # init list_data
                list_data = []
                for octet in range (0,msg["dlc"]):
                    octet = randint(0,255)
                    list_data.append(octet)
                can_msg  = Frame(id_= id_dec, data=list_data, dlc = msg["dlc"], flags=canlib.MessageFlag.STD )               
                ch_a.write(can_msg)
        except Exception as e:
            print (e)
            raise
        time.sleep(0.1)
    pass

#Open a virtual channel
ch_a = canlib.openChannel(channel=0,flags=canlib.Open.ACCEPT_VIRTUAL) 
# use setBusParams() to set the canBitrate to 1M.
ch_a.setBusParams(canlib.canBITRATE_1M)
# Channel ready to receive and send messages.
ch_a.busOn()
#handleur dbc
database = cantools.database.load_file("DBC_VCU_V2.dbc")
#list 
list_100ms = []
list_500ms = []
list_1000ms = []
#dict
d_100ms = {}
d_500ms = {}
d_1000ms = {}

#decode le DBC 
#enregistre les id en fonction de la période des trames
for msg in database.messages:
    id = msg.frame_id
    cycle = msg.cycle_time
    dlc = msg.length
    if cycle == 100 :
        d_500ms = {"id": id , "dlc":dlc}
        list_500ms.append(d_500ms)
    elif cycle == 1000 :
        d_1000ms = {"id": id , "dlc":dlc}
        list_1000ms.append(d_1000ms)
    else:
        #cas le plus critique
        d_100ms = {"id": id , "dlc":dlc}
        list_100ms.append(d_100ms)
        #cas le moins critique
        #list_1000ms.append(id)


#Lance les threads
t_100ms = threading.Thread(target= send_can_dbc_100ms)
t_500ms = threading.Thread(target= send_can_dbc_500ms)
t_1000ms = threading.Thread(target= send_can_dbc_1000ms)
t_can2 = threading.Thread(target= send_can2)
t_can3 = threading.Thread(target= send_can3)
t_100ms.start()
t_500ms.start()
t_1000ms.start()
t_can2.start()
t_can3.start()
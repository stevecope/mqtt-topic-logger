#!c:\python34\python
#!python3
###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose
"""
This will log messages to file.Los time,message and topic as JSON data
"""
mqttclient_log=False #MQTT client logs showing messages
Log_worker_flag=True
import paho.mqtt.client as mqtt
import json
import os
import time
import sys, getopt,random
import logging
import tlogger 
import threading
from queue import Queue
from command import command_input
import command
import collections



q=Queue()

##helper functions
def convert(t):
    d=""
    for c in t:  # replace all chars outside BMP with a !
            d =d+(c if ord(c) < 0x10000 else '!')
    return(d)
###
def getheader(file_name):
    headers={}
    fp=open(file_name,'r')
    for line in fp:
        line=line.strip()
        #print("line =",line)
        data=line.split(",")
        x=data.pop(0)
        #print(data)
        headers[x]=data

    return headers
##############
class MQTTClient(mqtt.Client):#extend the paho client class
   run_flag=False #global flag used in multi loop
   def __init__(self,cname,**kwargs):
      super(MQTTClient, self).__init__(cname,**kwargs)
      self.topic_ack=[] #used to track subscribed topics
      self.subscribe_flag=False
      self.bad_connection_flag=False
      self.bad_count=0
      self.count=0
      self.connected_flag=False
      self.connect_flag=False #used in multi loop
      self.sub_topic=""
      self.sub_topics=[] #multiple topics
      self.sub_qos=0
      self.broker=""
      self.port=1883
      self.keepalive=60
      self.cname=""
      self.delay=10 #retry interval

def Initialise_clients(cname,mqttclient_log=False,cleansession=True,flags=""):
    #flags set

   logging.info("initialising clients")
   client= MQTTClient(cname,clean_session=cleansession)
   client.cname=cname
   client.on_connect= on_connect        #attach function to callback
   client.on_message=on_message        #attach function to callback
   if mqttclient_log:
      client.on_log=on_log
   return client

def on_connect(client, userdata, flags, rc):
   """
   set the bad connection flag for rc >0, Sets onnected_flag if connected ok
   also subscribes to topics
   """
   logging.debug("Connected flags"+str(flags)+"result code "\
    +str(rc)+"client1_id")

   if rc==0:
      client.connected_flag=True #old clients use this
      client.bad_connection_flag=False
      if client.sub_topic!="": #single topic
          logging.info("subscribing "+str(client.sub_topic))
          topic=client.sub_topic
          if client.sub_qos!=0:
              qos=client.sub_qos
              client.subscribe(topic,qos)
      elif client.sub_topics!="":

        client.subscribe(client.sub_topics)
        print("Connected and subscribed to ",client.sub_topics)

   else:
     client.bad_connection_flag=True #
     client.bad_count +=1
     client.connected_flag=False #
def on_message(client,userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    message_handler(client,m_decode,topic)
    #print("message received ",topic)
    
def message_handler(client,msg,topic):
    data=collections.OrderedDict()
    tnow=time.time()
    try:
        msg=json.loads(msg)#convert to Javascript before saving
        json_flag=True
    except:
        json_flag=False
        #print("not already json")

    s=time.localtime(tnow)

    year=str(s[0])
    month=s[1]
    if month <10:
        month="0"+str(month)
    day =s[2]
    if day<10:
        day="0"+str(day)
    hours=s[3]
    if hours<10:
        hours="0"+str(hours)
    m=s[4]
    if m<10:
        m="0"+str(m)
    sec=s[5]
    if sec<10:
        sec="0"+str(sec)

    ltime =str(year) + "-" + str(month) + "-" + str(day) + "_" + str(hours)
    ltime=ltime + ":" + str(m) + ":" + str(sec)
    #print("time ",ltime)
    data["time_ms"]=int(tnow*1000)
    data["time"]=ltime
    data["topic"]=topic
    if json_flag and csv_flag:
        keys=msg.keys()
        for key in keys:
            data[key]=msg[key]
    else:             
        data["message"]=msg


    if command.options["storechangesonly"]:
        if has_changed(client,topic,msg):
            client.q.put(data) #put messages on queue
    else:
        client.q.put(data) #put messages on queue

def has_changed_test(client,topic,msg):
    #used when testing the data log tester
    if topic in client.last_message:
        if client.last_message[topic]["status"]==msg["status"]:
            return False
    client.last_message[topic]=msg
    return True
    
def has_changed(client,topic,msg):
    #print("has changed ",options["testmode"])
    if topic in client.last_message:
        if client.last_message[topic]==msg:
            return False
    client.last_message[topic]=msg
    return True
###
def log_worker():
    """runs in own thread to log data from queue"""
    while Log_worker_flag:
        #print("worker running ",csv_flag)
        time.sleep(0.01)
        #time.sleep(2)
        while not q.empty():
            results = q.get()
            if results is None:
                continue
            if csv_flag:
                 log.log_data(results)
                 #print("message saved csv")
            else:
                log.log_json(results)
                #print("message saved json")
    log.close_file()
# MAIN PROGRAM
options=command.options

if __name__ == "__main__" and len(sys.argv)>=2:
    options=command_input(options)
else:
    print("Need broker name and topics to continue.. exiting")
    raise SystemExit(1)

#verbose=options["verbose"]

if not options["cname"]:
    r=random.randrange(1,10000)
    cname="logger-"+str(r)
else:
    cname="logger-"+str(options["cname"])
Levels=["DEBUG","INFO","WARNING","ERROR","CRITICAL"]

print("logging level ",options["loglevel"])
logging.basicConfig(level=options["loglevel"])
logging.basicConfig(level="INFO")
log_dir=options["log_dir"]


logging.info("creating client"+cname)

client=Initialise_clients(cname,mqttclient_log,False)#create and initialise client object
if options["username"] !="":
    client.username_pw_set(options["username"], options["password"])

client.sub_topics=options["topics"]
client.broker=options["broker"]
client.port=options["port"]


if options["JSON"]: #
    csv_flag=False
if options["csv"]:
    csv_flag=True
    options["JSON"]=False
    print("Logging csv format")
if options["JSON"]:
    print("Logging JSON format")
if options["storechangesonly"]:
    print("starting storing only changed data")
else:
    print("starting storing all data")
    
##
log=tlogger.T_logger(log_dir,options["log_records"],csv_flag)
print("Log Directory =",log_dir)
if options["header_flag"]: #

    file_name=options["fname"]
    headers={}
    headers=getheader(file_name)
    log.set_headers(headers)
    print("getting headers from ",file_name)
    #print(headers)
Log_worker_flag=True
t = threading.Thread(target=log_worker) #start logger
t.start() #start logging thread
###

client.last_message=dict()
client.q=q #make queue available as part of client



try:
    res=client.connect(client.broker,client.port)      #connect to broker
    print("connecting to broker",client.broker)
    client.loop_start() #start loop

except:
    logging.debug("connection failed")
    print("connection failed")
    client.bad_count +=1
    client.bad_connection_flag=True #old clients use this
#loop and wait until interrupted   
try:
    while True:
        time.sleep(1)
        pass

except KeyboardInterrupt:
    print("interrrupted by keyboard")

client.loop_stop() #start loop
Log_worker_flag=False #stop logging thread
time.sleep(5)


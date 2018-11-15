#!python3
###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
###Free to use for any purpose
import sys, getopt
options=dict()

##EDIT HERE ###############
options["username"]=""
options["password"]=""
options["broker"]="127.0.0.1"
options["port"]=1883
options["verbose"]=True
options["cname"]=""
options["topics"]=[("",0)]
options["storechangesonly"]=True
options["testmode"]=False
options["loglevel"]=3
options["log_dir"]="tlogs"
options["log_records"]=5000
options["number_logs"]=0

#Test mode was introduced because when using a test generator
#we need to add various counters to message so as to track it.
#This meas that even though the real message doesn't change
#the overall message does. The data logger when in test mode ignores
#the counters in the message and looks only at the status field
#which contains the actual data.
def command_input(options={}):
    topics_in=[]
    qos_in=[]

    valid_options=" --help <help> -h or -b <broker> -p <port>-t <topic> -q QOS -v <verbose> -h <help>\
 -L logging level 0-5 ,Debug,Info,Warning,Error,critical)  -n Client ID or Name -u Username -P Password -s <store all data>\
-l <log directory default= mlogs> \
-T test mode used when using tester and with log ony changes as true"
    print_options_flag=False
    try:
      opts, args = getopt.getopt(sys.argv[1:],"h:b:p:t:q:l:vsTn:u:P:l:L:")
    except getopt.GetoptError:
      print (sys.argv[0],valid_options)
      sys.exit(2)
    qos=0

    for opt, arg in opts:
        if opt == '-h':
             options["broker"] = str(arg)
        elif opt == "-b":
             options["broker"] = str(arg)
        elif opt == "-T":
             options["testmode"] = True
        elif opt =="-p":
            options["port"] = int(arg)
        elif opt =="-t":
            topics_in.append(arg)
        elif opt =="-q":
             qos_in.append(int(arg))
        elif opt =="-n":
             options["cname"]=arg
        elif opt =="-L":
            options["loglevel"]=int(arg)
        elif opt == "-P":
             options["password"] = str(arg)
        elif opt == "-u":
             options["username"] = str(arg)
        elif opt =="-v":
            options["verbose"]=True
        elif opt =="-s":
            options["storechangesonly"]=False
        elif opt =="-l":
            options["log_dir"]=str(arg)



    lqos=len(qos_in)
    for i in range(len(topics_in)):
        if lqos >i:
            topics_in[i]=(topics_in[i],int(qos_in[i]))
        else:
            topics_in[i]=(topics_in[i],0)

    if topics_in:
        options["topics"]=topics_in #array with qos
    return options

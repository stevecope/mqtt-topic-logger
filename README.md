
Simple Python MQTT Data Logger by Topic

.
This software monitors a group of topics and creates a log file 
for each topic to which this MQTT client has subscribed.


You can specify the root log directory when starting defaults to tlogs

.

Default log size is 5MB
You need to provide the script with:

    List of topics to monitor
    broker name and port
    username and password if needed.
    base log directory and number of logs have defaults
Valid command line Options:
--help <help>
-h <broker> 
-b <broker> 
-p <port>
-t <topic> 
-q <QOS>
-v <verbose>
-d logging debug 
-n <Client ID or Name>
-u Username 
-P Password
-s <store all data>\
-l <log directory default= tlogs> 
-T test mode when use with the data logger tester
-r Record size in bytes default=10000
-c log in csv format
-f -f filename of header file default is data.csv

	Example Usage:

You will always need to specify the broker name or IP address 
and the topics to log

Note: you may not need to use the python prefix or may 
need to use python3 mqtt-topic-logger.py (Linux)

Specify broker and topics 

    python mqtt-topic-logger.py -h 192.168.1.157 -t sensors/#

Specify broker and multiple topics

    python mqtt-topic-logger.py -h 192.168.1.157 -t sensors/# -t  home/#
	

Log All Data:

    python mqtt-topic-logger.py -h 192.168.1.157 -t sensors/# -s 

Specify the client name used by the logger

    python mqtt-topic-logger.py -h 192.168.1.157 -t sensors/# -n data-logger

Specify the log directory

    python mqtt-topic-logger.py -h 192.168.1.157 -t sensors/# -l mylogs
	
Log in CSV format

    python mqtt-topic-logger.py -h 192.168.1.157 -t sensors/# -c

 Log in CSV format and use data.csv header file

    python mqtt-topic-logger.py -h 192.168.1.157 -t sensors/# -c -f data.csv
---------
Logger Class

The class is implemented in a module called tlogger.py (topic logger).

To create an instance you ca supply two parameters:

    The log directory- defaults to tlogs
    Max Log Size defaults to 5MB
 

log=tlogger.T_logger(log_dir)

The logger creates the log files in the directory using the topic names for the directory names and log files starting with log000.txt
When the file reaches 5Mb it is rotated

 log data  is JSON format with a timestamp added to the message


The logger will return True if successful and False if not.

To prevent loss of data in the case of computer failure the logs are continuously flushed to disk .

The logger will not clear log files when you start the logger you should ensure the log directory is empty.
When logging  to a csv file you can change the default header order using a header file.
Each topic requires its own header entry. Below is an example header file:

test/sensor1,time_ms,time,ms,Urms,Umin,Umax
test/sensor2,time_ms,time,ms,Urms,Umin,Umax
test/sensor3,time_ms,time,sensor,count,status
test/sensor4,time_ms,time,ms,Urms,Umin,Umax,count

You can see that topics sensor1 and sensor2 use the same header whereas sensor3 and sensor4 have different headers.

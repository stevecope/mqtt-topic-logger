
Simple Python MQTT Data Logger by Topic

.
This software monitors a group of topics and creates a log file 
for each topic to which this MQTT client has subscribed.


You can specify the root log directory when starting

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
-l <log directory default= mlogs> 
-T test mode when use with the data logger tester

	Example Usage:

You will always need to specify the broker name or IP address 
and the topics to log

Note: you may not need to use the python prefix or may 
need to use python3 mqtt_data_logger.py (Linux)

Specify broker and topics 

    python mqtt_data_logger.py -b 192.168.1.157 -t sensors/#

Specify broker and multiple topics

    python mqtt_data_logger.py -b 192.168.1.157 -t sensors/# -t  home/#
	

Log All Data:

    python mqtt_data_logger.py b 192.168.1.157 -t sensors/# -s 

Specify the client name used by the logger

    python mqtt_data_logger.py b 192.168.1.157 -t sensors/# -n data-logger

Specify the log directory

    python mqtt_data_logger.py b 192.168.1.157 -t sensors/# -l mylogs
 
---------
Logger Class

The class is implemented in a module called tlogger.py (topic logger).

To create an instance you ca supply two parameters:

    The log directory- defaults to tlogs
    Max Log Size defaults to 5MB
 

log=tlogger.T_logger(log_dir)

The logger creates the log files in the directory using the topic names for the directory names and log files starting with log000.txt

 log data  is JSON format with a timestamp added to the message


The logger will return True if successful and False if not.

To prevent loss of data in the case of computer failure the logs are continuously flushed to disk .

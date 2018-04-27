
# Python Module to Log MQTT data by Topic

This software monitors a group of topics and creates a logfile
for each topic to which this MQTT client has subscribed. You can specify the log directory when starting.  When the log file reaches a certain size, it rotates the logs. 

## Our Vision
MQTT is a tree of topics.  An obvious way to store the data, particularly for chat, is as a tree on the filesystem.  Specifically, with each topic as a directory. Subtopics are subdirectories. For each topic,  we have a file where the current data is written.  When the file gets too large, we “rotate the logs” meaning we close the file, add a version number to the file name, open a new file and continue recording the data.  

The key idea is that the MQTT topic tree structure and the file system structure are identical, they just have different roots. 

This structure makes life very easy for the developer.  When someone wants the most recent history for an MQTT topic, they know exactly where to look.  For additional history just ask for the most recent version of that file.  To delete a topic, just delete that branch of the file system.  To move a topic, just move that branch of the file system. All very easy for the developer.

## Performance
The performance we care most about is speed of response to user queries.  When a user loads a chat room, we want the server to load the chat history as fast as possible. We want all the chat history in its own file, so that NGINX can load it without the server having to index a large data file. 

## Scalability
If you need scalability, then it is 
pretty easy to split this model across multiple Python processes, even multiple computers.  Just assign a different branch of the tree to a different mqtt-topic-logging process.  If they are on different computers, then it is easy to merge the file system trees into a single effective tree.   There are several ways to do that.      You can mount all the files in a single NFS file system.  Or you can serve different branches of the tree from different computers. 


## Project Status 
This started off as a Python project to log data to a single file.   Now it logs data to multiple files, but all in a single directory.    We recently realized that the MQTT world wants a topic tree of files, and so we are busy implementing ti. 

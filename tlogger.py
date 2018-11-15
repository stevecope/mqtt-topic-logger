import time,os,json,logging
class T_logger():
    def __init__(self,log_dir="tlogs",MAX_LOG_SIZE=5000000):
        self.MAX_LOG_SIZE=MAX_LOG_SIZE
        self.log_root_dir=log_dir
        self.topics={}#key=topic name\
        #data is array[file pointer,directory,counter]
        self.create_log_dir(self.log_root_dir)
        print("Max log size= ",MAX_LOG_SIZE)


    def __flushlogs(self,fo): # write to disk 
        fo.flush()
        os.fsync(fo.fileno())

    def create_log_dir(self,log_dir):
        try:
            os.stat(log_dir)
        except:
            os.mkdir(log_dir) 

    def close_files(self):
        for key in self.topics:
            fo=self.topics[key]
            if not fo.closed:
                fo.close()
    def write(self,fo,data):
        try:
            fo.write(data)
            self.__flushlogs(fo)
        except BaseException as e:
            logging.error("Error on_data: %s" % str(e))
            return False
    def update_topic_counter(topic,count):
        pass
     
                                                                                         
    def create_log_file(self,dir,topic,fo="",count=0):

        log_numbr="{0:003d}".format(count)
        logging.info("log number "+str(log_numbr)+ "  dir "+dir)
        filename= "log"+str(log_numbr)+".txt"
        try:
            os.stat(filename)
            os.remove(filename)#remove old log if exists
        except:
            pass
        filename=dir+"/"+filename
        logging.info("Creating log "+str(count))

        if count==0:
            pass   
        else:
            fo.close() #close old log file

        #update_topic_counter(topic,count)
        fo=open(filename, 'w')
        count+=1
        self.topics[topic]=[fo,dir,filename,count]
        return fo


    def log_json(self,data):
        topic=data["topic"] #get topic from data
        del data["topic"] #no need to store topic
        jdata=json.dumps(data)+"\n"
        self.log_data(jdata,topic)    
    def log_data(self,data,topic=""):
        if topic=="":
            topic=data["topic"]
            del data["topic"] #no need to store topic
        if topic in self.topics:
            fo=self.topics[topic][0] #retrieve pointer
            self.write(fo,data)
            file=self.topics[topic][2]
            if os.stat(file).st_size>self.MAX_LOG_SIZE:
                dir=self.topics[topic][1]
                count=self.topics[topic][3]
                fo=self.create_log_file(dir,topic,fo,count)
                self.topics[topic][0]=fo
        else:
            s_topics=topic.split('/')
            dir=self.log_root_dir
            for t in s_topics:
                dir=dir+"/"+t
                self.create_log_dir(dir)
            fo=self.create_log_file(dir,topic,fo="",count=0)

            self.write(fo,data)


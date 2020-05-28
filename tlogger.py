import time,os,json,logging,csv
class T_logger():
    def __init__(self,log_dir="tlogs",MAX_LOG_SIZE=5000,csv_flag=False):
        self.MAX_LOG_SIZE=MAX_LOG_SIZE
        self.log_root_dir=log_dir
        self.topics={}#key=topic name\
        #data is array[file pointer,directory,counter]
        self.create_log_dir(self.log_root_dir)
        print("Max log size= ",MAX_LOG_SIZE)
        self.columns = ['time','message']#needed as get error when storing json
        self.csv_flag = csv_flag
        self.header_flag=False

    def set_headers(self,headers):

        self.headers = headers
        self.header_flag=True


    def __flushlogs(self,fo): # write to disk 
        fo.flush()
        os.fsync(fo.fileno())

    def create_log_dir(self,log_dir):
        try:
            os.stat(log_dir)
        except:
            os.mkdir(log_dir) 

    def close_file(self):
        for key in self.topics:
            fo=self.topics[key][0]
            if not fo.closed:
                fo.close()
    def write(self,fo,data,writer):
        if(self.csv_flag):
                logging.info("writing csv  =",data)
                writer.writerow(data)
        else:
            try:
                fo.write(data)
            except BaseException as e:
                logging.error("Error on_data: %s" % str(e))
                return False
        self.__flushlogs(fo)
    def update_topic_counter(topic,count):
        pass
     
                                                                                         
    def create_log_file(self,dir,topic,columns,fo="",count=0):

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
        writer=csv.DictWriter(fo,\
                                   fieldnames=columns,quoting=csv.QUOTE_MINIMAL)
        self.topics[topic]=[fo,dir,filename,count,writer]
        if self.csv_flag:
            writer.writeheader() 
        return (fo,writer)


    def log_json(self,data):
        topic=data["topic"] #get topic from data
        del data["topic"] #no need to store topic
        jdata=json.dumps(data)+"\n"
        self.log_data(jdata,topic)    
    def log_data(self,data,topic=""):
        columns=0 #needed as json data causes error
        if topic=="":
            topic=data["topic"]
            del data["topic"] #no need to store topic
        if self.csv_flag :
            if(self.header_flag):
                #print("topic = ",topic)
                if topic in self.headers:
                    columns=self.headers[topic]
                    
                else:
                    columns=list(data.keys())
            
            else:
                columns=list(data.keys())
 

        if topic in self.topics:

 
            fo=self.topics[topic][0] #retrieve pointer
            writer=self.topics[topic][4] #retrieve pointer
            self.write(fo,data,writer)
            file=self.topics[topic][2]
            if os.stat(file).st_size>self.MAX_LOG_SIZE:
                dir=self.topics[topic][1]
                count=self.topics[topic][3]
                fo,writer=self.create_log_file(dir,topic,columns,fo,count)
                self.topics[topic][0]=fo
                self.topics[topic][4]=writer
        else:

            s_topics=topic.split('/')
            dir=self.log_root_dir
            for t in s_topics:
                dir=dir+"/"+t
                self.create_log_dir(dir)
            fo,writer=self.create_log_file(dir,topic,columns,fo="",count=0)
            self.topics[topic][0]=fo
            self.topics[topic][4]=writer
            self.write(fo,data,writer)



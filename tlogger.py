import time,os,json,logging,csv
#doesn't use writer
class T_logger():
    def __init__(self,log_dir="tlogs",MAX_LOG_SIZE=5000,csv_flag=False):
        self.MAX_LOG_SIZE=MAX_LOG_SIZE
        self.log_root_dir=log_dir
        self.metafile="metafile.txt"
        self.topics={}#key=topic name\
        #data is array[file pointer,directory,counter]
        self.create_log_dir(self.log_root_dir)
        print("Max log size= ",MAX_LOG_SIZE)
        self.columns = ['time','message']#needed as get error when storing json
        self.csv_flag = csv_flag
        self.header_flag=False
    def write_header(self,fo,columns):
        self.header_flag=True
        try:
            fo.write(columns)
            fo.write("\n")
        except BaseException as e:
            logging.error("Error on_data: %s" % str(e))
            return False
        self.__flushlogs(fo)

    def set_headers(self,headers):
        #not currently used
        self.headers = headers
        self.header_flag=True
    def extract_columns(self,data):
        columns=""

        #data=flatten_dict(msg)
        for key in data:
            #print("key =",key)
            if columns =="":
                columns=key
            else:
                columns=columns+","+key
        #print(columns)
        return(columns)
    def extract_data(self,data):
        line_out=""
        for key in data:
            #print("here ",data[key])
            if line_out =="":
                line_out=str(data[key])
            else:
                line_out=line_out+","+str(data[key])
        #print(line_out)
        return(line_out)

    def __flushlogs(self,fo): # write to disk 
        fo.flush()
        os.fsync(fo.fileno())

    def create_log_dir(self,log_dir):
        try:
            os.stat(log_dir)
        except:
            os.mkdir(log_dir) 

    def close_file(self):
        print("closing files ")

        for key in self.topics:
            fo=self.topics[key][0]
            if not fo.closed:
                fo.close()
    def write(self,fo,data):
        if self.csv_flag:
            data=self.extract_data(data)
        try:
            fo.write(data)
            fo.write("\n")
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

        self.topics[topic]=[fo,dir,filename,count,columns]
        return (fo)


    def log_json(self,data):
        topic=data["topic"] #get topic from data
        del data["topic"] #no need to store topic
        jdata=json.dumps(data)
        self.log_data(jdata,topic)    
    def log_data(self,data,topic=""):
        columns=0 #needed as json data causes error
        if topic=="":
            topic=data["topic"]
            del data["topic"] #no need to store topic


        if topic in self.topics:
 
            fo=self.topics[topic][0] #retrieve pointer
            #writer=self.topics[topic][4] #retrieve pointer
            self.write(fo,data)
            file=self.topics[topic][2]
            #need to create new log file
            if os.stat(file).st_size>self.MAX_LOG_SIZE:
                dir=self.topics[topic][1]
                count=self.topics[topic][3]
                fo=self.create_log_file(dir,topic,columns,fo,count)
                if self.csv_flag:
                    columns=self.extract_columns(data)
                    self.write_header(fo,columns)
                self.topics[topic][0]=fo
                self.topics[topic][4]=columns
                #self.write(fo,data)
        else:
            #store file name and pointers

            s_topics=topic.split('/')
            dir=self.log_root_dir
            for t in s_topics:
                dir=dir+"/"+t
                self.create_log_dir(dir)
            fo=self.create_log_file(dir,topic,columns,fo="",count=0)
            if self.csv_flag:
                columns=self.extract_columns(data)
                self.write_header(fo,columns)
            self.topics[topic][0]=fo
            self.topics[topic][4]=columns
            self.write(fo,data)



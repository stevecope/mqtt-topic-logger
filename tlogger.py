import time,os,json,logging
class T_logger():
    def __init__(self,log_dir="tlogs"):
        self.log_dir=log_dir
        self.count=0
        self.create_log_dir()
        self.topics={}
    def __flushlogs(self,fo): # write to disk 
        fo.flush()
        logging.info("flushing logs")
        os.fsync(fo.fileno())

    def create_log_dir(self):
        try:
            os.stat(self.log_dir)
        except:
            os.mkdir(self.log_dir) 

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
    def log_json(self,data):
        topic=data["topic"]
        jdata=json.dumps(data)+"\n"
        self.log_data(jdata,topic)                                                                                          
                                                                                         

    def log_data(self,data,topic=""):
        if topic=="":
            topic=data["topic"]
        if topic in self.topics:
            #print("topic exists")
            fo=self.topics[topic]
            self.write(fo,data)

        else:
            filename=topic.replace("/","-_-")
            filename=self.log_dir+"/"+filename+".txt"
            fo=open(filename, 'a')
            self.topics[topic]=fo
            self.write(fo,data)


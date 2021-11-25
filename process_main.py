from threading import Thread
import os, pathlib, pymongo
from datetime import datetime


""" Declaring some constants for threads"""
PROCESSING_DIRECTORY = "Processing"
QUEUE_DIRECTORY = "Queue"
PROCESSED_DIRECTORY = "Processed"

def initialize_db():
    """ Set-up MongoDB for inserting individual data """
    try:
        DB_Client = pymongo.MongoClient("mongodb://localhost:27017/")
        ProcessDB = DB_Client["ProcessDB"]
        ProcessCollection = ProcessDB["ProcessCollection"]
        
    except Exception as e:
        print (str(e), ":: DB failed can't run Threads")
        ProcessCollection = None
    return ProcessCollection

def Processing(ProcessCollection):
    """ For creating a process file in Processing folder and inserting in db """
    while True:
        current_time = datetime.now().isoformat(timespec='seconds').replace("-","_").replace(":","_")
        current_filename = os.path.join(PROCESSING_DIRECTORY, current_time) + '.txt'

        with open(current_filename, 'w') as f:
            f.write(current_time)
        ProcessCollection.insert_one({"ProcessId" : current_time,
                                      "Status":0,
                                    })
        print (current_time)
        os.system("sleep 1")

def Queue():
    """ Checking if Queue is empty or not if not than For moving files from 
        Processing directory to Queue directory
    """
    
    while True:
        if len(os.listdir(QUEUE_DIRECTORY)) > 0:
            continue
        
        oldfiles = os.listdir(PROCESSING_DIRECTORY)
        for files in oldfiles:
            os.replace(os.path.join(PROCESSING_DIRECTORY, files) , os.path.join(QUEUE_DIRECTORY, files))
            
        os.system("sleep 5")
    
def Processed(ProcessCollection):
    """ Move files from Queue directory to Processed file and update ProcessId to db """

    while True:
        oldfiles = os.listdir(QUEUE_DIRECTORY)
        for files in oldfiles:
            os.replace(os.path.join(QUEUE_DIRECTORY, files), os.path.join(PROCESSED_DIRECTORY, files))
            ProcessCollection.update_one({"ProcessId": files.split(".")[0]} ,
                                         {"$set":{ "Status": 1}
                                        })

if __name__ == "__main__":
    ProcessCollection = initialize_db()  # init db
    if not ProcessCollection: #exit from program if db not intialised
        exit(-1)

    # Thread declaration and passing specific arguments  
    processing = Thread(target = Processing, args = (ProcessCollection,),)
    queue = Thread(target = Queue)
    processed = Thread(target = Processed, args = (ProcessCollection,),)

    # Starting all threads
    processing.start()
    queue.start()
    processed.start()

    # Joining threads which will to make all threads and program to exit at the same time 
    processing.join()
    queue.join()
    processed.join()

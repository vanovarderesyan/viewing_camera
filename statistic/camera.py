import cv2
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6
import cv2, time, pandas 
# importing datetime class from datetime library 
from datetime import datetime 
from typing import Awaitable
import asyncio
from functools import wraps, partial
from .models import Motion
import threading
import time

def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run 

@async_wrap 
def detect_camera():
    print('mtav',Motion.objects.all())
    # Assigning our static_back to None 
    static_back = None
    
    # List when any moving object appear 
    motion_list = [ None, None ] 
    
    # Time of movement 
    time = [] 
    
    # Initializing DataFrame, one column is start  
    # time and other column is end time 
    df = pandas.DataFrame(columns = ["Start", "End"]) 

    print(df)

    time_count = 0
    # Capturing video 
    video = cv2.VideoCapture('rtsp://admin:@Admin10@192.168.1.103:554/Streaming/Channels/101')

    while True: 
        time_count = time_count +1 

        # if time_count == 60:
        #     break
        # Reading frame(image) from video 
        # print(video)
        check, frame = video.read() 
        # print(frame,check)
    
        # Initializing motion = 0(no motion) 
        motion = 0
    
        # Converting color image to gray_scale image 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    
        # Converting gray scale image to GaussianBlur  
        # so that change can be find easily 
        gray = cv2.GaussianBlur(gray, (21, 21), 0) 
    
        # In first iteration we assign the value  
        # of static_back to our first frame 
        if static_back is None: 
            static_back = gray 
            continue
    
        # Difference between static background  
        # and current frame(which is GaussianBlur) 
        diff_frame = cv2.absdiff(static_back, gray) 
    
        # If change in between static background and 
        # current frame is greater than 30 it will show white color(255) 
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1] 
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 
    
        # Finding contour of moving object 
        cnts,_ = cv2.findContours(thresh_frame.copy(),  
                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    
        for contour in cnts: 
            # print(cv2.contourArea(contour))
            if cv2.contourArea(contour) < 10000: 
                continue
            motion = 1
    
            (x, y, w, h) = cv2.boundingRect(contour) 
            # making green rectangle arround the moving object 
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3) 
    
        # Appending status of motion 
        motion_list.append(motion) 
    
        motion_list = motion_list[-2:] 
    

        # Appending Start time of motion 
        if motion_list[-1] == 1 and motion_list[-2] == 0: 
            time.append(datetime.now())
            print(datetime.now(),'start') 
    
        # Appending End time of motion 
        if motion_list[-1] == 0 and motion_list[-2] == 1: 
            Motion.objects.create(start_time=datetime.now(),end_time=time[-1],camera_index=1)
            time.append(datetime.now()) 
            print(datetime.now(),'end')


    
        # Displaying image in gray_scale 
        # cv2.imshow("Gray Frame", gray) 
    
        # # Displaying the difference in currentframe to 
        # # the staticframe(very first_frame) 
        # cv2.imshow("Difference Frame", diff_frame) 
    
        # # Displaying the black and white image in which if 
        # # intensity difference greater than 30 it will appear white 
        # cv2.imshow("Threshold Frame", thresh_frame) 
    
        # Displaying color frame with contour of motion of object 
        cv2.imshow("Color Frame", frame) 
    
        key = cv2.waitKey(1) 
        # if q entered whole process will stop 
        if key == ord('q'): 
            # if something is movingthen it append the end time of movement 
            if motion == 1: 
                time.append(datetime.now()) 
            break

    # Appending time of motion in DataFrame 
    print(time)
    for i in range(0, len(time), 2): 

        df = df.append({"Start":time[i], "End":time[i + 1]}, ignore_index = True) 
    
    # Creating a CSV file in which time of movements will be saved 
    df.to_csv("Time_of_movements.csv") 
    
    video.release() 
  
# Destroying all the windows 
cv2.destroyAllWindows() 
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('rtsp://admin:@Admin10@192.168.1.103:554/Streaming/Channels/101')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        # face_rects=face_cascade.detectMultiScale(gray,1.3,5)
        # for (x,y,w,h) in face_rects:
        # 	cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        # 	break
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


class VideoCamera1(object):
    def __init__(self):
        self.video = cv2.VideoCapture('rtsp://admin:@Admin10@192.168.1.103:554/Streaming/Channels/101')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        # # face_rects=face_cascade.detectMultiScale(gray,1.3,5)
        # for (x,y,w,h) in face_rects:
        # 	cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        # 	break
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

# asyncio.run(detect_camera())


class ThreadingCamera(object):
    """ Threading Camera class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, url=''):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.url = url
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        print('mtav',Motion.objects.all())
        # Assigning our static_back to None 
        static_back = None
        
        # List when any moving object appear 
        motion_list = [ None, None ] 
        
        # Time of movement 
        time = [] 
        
        # Initializing DataFrame, one column is start  
        # time and other column is end time 
        df = pandas.DataFrame(columns = ["Start", "End"]) 

        print(df)
        print(self.url,'--------------------')

        time_count = 0
        # Capturing video 
        video = cv2.VideoCapture(self.url)

        while True: 
            time_count = time_count +1 

            # if time_count == 60:
            #     break
            # Reading frame(image) from video 
            # print(video)
            check, frame = video.read() 
            # print(frame,check)
        
            # Initializing motion = 0(no motion) 
            motion = 0
        
            # Converting color image to gray_scale image 
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        
            # Converting gray scale image to GaussianBlur  
            # so that change can be find easily 
            gray = cv2.GaussianBlur(gray, (21, 21), 0) 
        
            # In first iteration we assign the value  
            # of static_back to our first frame 
            if static_back is None: 
                static_back = gray 
                continue
        
            # Difference between static background  
            # and current frame(which is GaussianBlur) 
            diff_frame = cv2.absdiff(static_back, gray) 
        
            # If change in between static background and 
            # current frame is greater than 30 it will show white color(255) 
            thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1] 
            thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 
        
            # Finding contour of moving object 
            cnts,_ = cv2.findContours(thresh_frame.copy(),  
                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        
            for contour in cnts: 
                # print(cv2.contourArea(contour))
                if cv2.contourArea(contour) < 10000: 
                    continue
                motion = 1
        
                (x, y, w, h) = cv2.boundingRect(contour) 
                # making green rectangle arround the moving object 
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3) 
        
            # Appending status of motion 
            motion_list.append(motion) 
        
            motion_list = motion_list[-2:] 
        

            # Appending Start time of motion 
            if motion_list[-1] == 1 and motion_list[-2] == 0: 
                time.append(datetime.now())
                print(datetime.now(),'start') 
        
            # Appending End time of motion 
            if motion_list[-1] == 0 and motion_list[-2] == 1: 
                Motion.objects.create(start_time=datetime.now(),end_time=time[-1],camera_index=1)
                time.append(datetime.now()) 
                print(datetime.now(),'end')


        
            # Displaying image in gray_scale 
            # cv2.imshow("Gray Frame", gray) 
        
            # # Displaying the difference in currentframe to 
            # # the staticframe(very first_frame) 
            # cv2.imshow("Difference Frame", diff_frame) 
        
            # # Displaying the black and white image in which if 
            # # intensity difference greater than 30 it will appear white 
            # cv2.imshow("Threshold Frame", thresh_frame) 
        
            # Displaying color frame with contour of motion of object 
            cv2.imshow("Color Frame", frame) 
        
            key = cv2.waitKey(1) 
            # if q entered whole process will stop 
            if key == ord('q'): 
                # if something is movingthen it append the end time of movement 
                if motion == 1: 
                    time.append(datetime.now()) 
                break

        # Appending time of motion in DataFrame 
        print(time)
        for i in range(0, len(time), 2): 

            df = df.append({"Start":time[i], "End":time[i + 1]}, ignore_index = True) 
        
        # Creating a CSV file in which time of movements will be saved 
        df.to_csv("Time_of_movements.csv") 
        
        video.release() 

def init():
    print('mt--------------------av',Motion.objects.all())

    ThreadingCamera('rtsp://admin:@Admin10@192.168.1.103:554/Streaming/Channels/101')
    ThreadingCamera('rtsp://admin:@Admin10@192.168.1.103:554/Streaming/Channels/101')
    ThreadingCamera('rtsp://admin:@Admin10@192.168.1.103:554/Streaming/Channels/101')
    ThreadingCamera('rtsp://admin:@Admin10@192.168.1.103:554/Streaming/Channels/101')
    ThreadingCamera('rtsp://admin:@Admin10@192.168.1.103:554/Streaming/Channels/101')
    ThreadingCamera('rtsp://admin:@Admin10@192.168.1.103:554/Streaming/Channels/101')
    ThreadingCamera('rtsp://admin:@Admin10@192.168.1.103:554/Streaming/Channels/101')

    return 1
init()

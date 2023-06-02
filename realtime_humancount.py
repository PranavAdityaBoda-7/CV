import cv2 # IMPORT THE PACKAGES
import imutils
import numpy as np
import argparse

def count_frame(frame): # function to detect 
    bounding_box, w =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03) # declare a bounding box
    
    person = 0 # intilayy declare number of persons as zero
    for x,y,w,h in bounding_box: #for every person in bounding box
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)#highlight the rectangle part of image with persons 
        cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)#identify the persons in the frame
        person += 1#increment the number of persons
    
    cv2.putText(frame, 'Counting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)# print the text as counting in image
    cv2.putText(frame, f'Total Persons : {person}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)#print the total number of persons in frame 
    cv2.imshow('output', frame) #print the frame with number of persons and persons highlighted
    return frame#return the frame with number of persons and persons highlighted

def find_video(path, path2): #function to find video with to arguments path, path2
    video = cv2.VideoCapture(path) # store the video in the video variable by taking path
    check, frame = video.read() #read the video into the frame
    while video.isOpened(): # while the video is opened
        check, frame =  video.read() #read te video into the frame

        if check: # if check is true 
            frame = imutils.resize(frame , width=min(800,frame.shape[1])) # resize the frame of the video
            frame = count_frame(frame) #detect the frame
            
            if path2 is not None: # if path 2 is not none
                path2.write(frame) # write the frame into the path2
            
            key = cv2.waitKey(1) # take the wait key
            if key== ord('q'): #if suppose th ekey is same as ASCII value of q then break
                break
        else:
            break
    video.release()#release the video
    cv2.destroyAllWindows() # destroy all the windows in the cv2

def find_image(path, output_path):#function to find image with to arguments path, output_path
	image = cv2.imread(path)#read the image from the path
	image = imutils.resize(image, width=min(600, image.shape[1]))#resize th eimage in imutils
	(regions, _) = HOGCV.detectMultiScale(image,winStride=(6, 6), padding=(4, 4), scale=1.05)#detect the multiscale 
	person=0
	for (x, y, w, h) in regions: #for each person in the region
		cv2.rectangle(image, (x, y), (x + w, y + h),(0, 0, 255), 2)#highlight the rectangle part of image with persons 
		cv2.putText(image, f'person {person}', (x,y), cv2.FONT_HERSHEY_PLAIN, 0.5, (0,0,255), 1) #identify the persons in the frame
		person += 1# increment the persons by 1
	
	# Showing the output Image
	cv2.putText(image, f'Total Persons : {person}', (50,50), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255,0,0),1)# Print the number of persons in the frame
	cv2.imshow("Image", image)# show the output image with number of persons and persons identified in rectangular blocks
	cv2.waitKey(0)#take the wait key
	cv2.destroyAllWindows() #destroy all the windows in cv2


def parse(): # declare the parse function
    arg_parse = argparse.ArgumentParser()#it is the argument given in the terminal command prompt
    arg_parse.add_argument("-v", "--video", default=None, help="video path") # if it is -v , then it is video
    arg_parse.add_argument("-i", "--image", default=None, help="image path") # if it is -i then it is image
    arg_parse.add_argument("-o", "--output", type=str, help="output")# if it is -o , then it is output
    args = vars(arg_parse.parse_args()) 

    return args # return the args
    
if _name_ == "_main_":
    HOGCV = cv2.HOGDescriptor()#take the HOG descriptor
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())# set the SVM detector in the HOGCV
    args = parse()# take the arguments in the terminal command
    image_path = args["image"]#take the path of image
    video_path = args['video']#take the path of video

    writer = None
    if args['output'] is not None and image_path is None:
        writer = cv2.VideoWriter(args['output'],cv2.VideoWriter_fourcc(*'MJPG'), 10, (600,600))

    if video_path is not None:# if the video path is not none then get the total persons in each frame in video and ignore the image
        find_video(video_path, writer)#find human count for each frame in video
    elif image_path is not None:#if the image path is not none then get the total persons in image  and ignore the video
        find_image(image_path, args['output'])#find human count for image
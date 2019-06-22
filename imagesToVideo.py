# Source: https://www.life2coding.com/convert-image-frames-video-file-using-opencv-python/
# importing libraries 
import os 
import json
import cv2  
from PIL import Image  
import sys
  
  
  

# Rezises all images to the same scale for video's sake
def reszieImages(path):
    os.chdir(path)   
    mean_height = 0
    mean_width = 0
    num_of_images = len(os.listdir('.')) 
    
    # Gets measurements
    for file in os.listdir('.'): 
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"): 
            im = Image.open(os.path.join(path, file)) 
            width, height = im.size 
            mean_width += width 
            mean_height += height 
            # im.show()   # uncomment this for displaying the image 
    
    # Finding the mean height and width of all images. 
    # This is required because the video frame needs 
    # to be set with same width and height. Otherwise 
    # images not equal to that width height will not get  
    # embedded into the video 
    mean_width = int(mean_width / num_of_images) 
    mean_height = int(mean_height / num_of_images) 
    
    # Resizing of the images to give 
    # them same width and height  
    for file in os.listdir('.'): 
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"): 
            # opening image using PIL Image 
            im = Image.open(os.path.join(path, file))  
    
            # im.size includes the height and width of image 
            width, height = im.size    
            print(width, height) 
    
            # resizing  
            imResize = im.resize((mean_width, mean_height), Image.ANTIALIAS)  
            imResize.save( file, 'JPEG', quality = 95) # setting quality 
            # printing each resized image name 
            print(im.filename.split('\\')[-1], " is resized")  
  
# Video Generating function 
def createVideoFromFolder(path, fps, videoName): 
    reszieImages(path)
    image_folder = '.' # make sure to use your folder 
    

    # Gets and sorts images
    files = os.listdir(path)
    os.chdir(path)
    images = sorted(files, key=os.path.getatime)
    images = [img for img in images
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")] 

    print("Sorted images: " + str(images))

     
    # Array images should only consider 
    # the image files ignoring others if any 
    # print(images)  
  
    frame = cv2.imread(os.path.join(image_folder, images[0])) 
  
    # setting the frame width, height width 
    # the width, height of first image 
    height, width, layers = frame.shape   
    video = cv2.VideoWriter(videoName, 0, fps, (width, height))  
  
    # Appending the images to the video one by one 
    for image in images:  
        video.write(cv2.imread(os.path.join(image_folder, image)))  
      
    # Deallocating memories taken for window creation 
    cv2.destroyAllWindows()  
    video.release()  # releasing the video generated 
    print("Saved video as: " + str(videoName))
  
  
if __name__ == "__main__":
    folderPath = sys.argv[1]
    fps = sys.argv[2]
    videoName = sys.argv[3]

    # Calling the generate_video function 
    createVideoFromFolder(folderPath, fps, videoName) 
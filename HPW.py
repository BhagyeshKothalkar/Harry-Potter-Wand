import cv2 as cv
import numpy as np
import time

#drawing = False
points = np.empty((0, 2), dtype=np.uint8)
def empty(arg):
    pass
#cv.namedWindow("Trackbars")
#cv.resizeWindow("Trackbars", 640, 240)
# cv.createTrackbar("Hue Min", "Trackbars", 0, 179,empty)
# cv.createTrackbar("Hue Max", "Trackbars", 0, 179,empty)
# cv.createTrackbar("Sat Min", "Trackbars", 0, 255,empty)
# cv.createTrackbar("Sat Max", "Trackbars", 0, 255,empty)
# cv.createTrackbar("Val Min", "Trackbars", 0, 255,empty)
# cv.createTrackbar("Val Max", "Trackbars", 0, 255,empty)

cap = cv.VideoCapture(0)
def getContours(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 500:
            cv.drawContours(imgnew, cnt, -1, (255, 255 , 0), 3)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            print(area, peri, len(approx))
            x, y, w, h = cv.boundingRect(approx)
            print(x, y, w)
            cv.rectangle(imgnew, (x, y), (x + w, y + h), (255, 0, 255), 5)
    return x + w//2, y



while True: 
    
    success, img = cap.read()
    img = cv.circle(img, (140, 70), 6, (0, 255, 0), 2)
    img = cv.circle(img, (190, 140), 6, (0, 0, 255), 2)
    imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # h_min = cv.getTrackbarPos("Hue Min", "Trackbars")
    # h_max = cv.getTrackbarPos("Hue Max", "Trackbars")
    # s_min = cv.getTrackbarPos("Sat Min", "Trackbars")
    # s_max = cv.getTrackbarPos("Sat Max", "Trackbars")
    # v_min = cv.getTrackbarPos("Val Min", "Trackbars")
    # v_max = cv.getTrackbarPos("Val Max", "Trackbars")
    
    #97 119 121 185 51 111

    lower = np.array([0, 100, 100])
    upper = np.array([10, 255,255])
    mask = cv.inRange(imgHSV, lower, upper)

    img_blur = cv.GaussianBlur(mask, (7, 7), 0)
    #imgcanny = cv.Canny(img_blur, 50, 250)
    #imgdial = cv.dilate(imgcanny,np.ones((3,3)))
    imgnew = cv.cvtColor(img_blur,cv.COLOR_GRAY2BGR)
    x, y = getContours(mask)

    points = np.vstack((points, np.array([x, y])))
    if(points.shape[0]>100):
        if np.linalg.norm(points[-1]- points[-100]) < 200:
            print("End")
            break

   # We can start drawing once the contour coincided with the start circle ( this coincidence can be vhcked using the function cv2.pointPolygonTest(contour, start_circle_center,False)>= 0)
    #And end the drawing once the contour is in range of the end cirlce using the same function.
    #The function returns a positive value or zero if the center of circle is on or inside the contour.
    #snippet:
      #get contours using cv2.findContours and the use the above function to start drawing 
      #then once the contours coincides with end cirlce center break the loop
   #while True: 
     #success, frame = cap.read()
     #cv2.circle() start circle
     #cv2.circle() end circle
     #contours=_________
     #if cv2.pointPolygonTest:
        #loop for drawing circle
        #if pointPolygonTest with end circle then break;
    #NOW THE PROBLEM TO BE FIGURED OUT IS THE ORDER OF POSTIONING THESE LOOPS
     
        
    
    for point in points:
        cv.circle(imgnew, point, 10, (255, 0, 0), 3)




    # cv.imshow("og",img)
    # cv.imshow("HSV", imgHSV)
    # cv.imshow("mask", mask)
    # cv.imshow("Result",img_result)
    cv.imshow("img",imgnew)

    if cv.waitKey(1)& 0xff == ord('q'):
        cv.destroyAllWindows()
        #print(h_min, h_max, s_min, s_max, v_min, v_max,)
        break



# width, height,brightness = (1280, 720, 100)
# cap.set(3, width)
# cap.set(4, height)
# cap.set(10, 100)

# while True:
#     success, img = cap.read()
#     if success:
#         cv.imshow("video", imgcanny)
#         if cv.waitKey(1) & 0xff == ord('q'):
#             break

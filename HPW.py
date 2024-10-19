import cv2 as cv
import numpy as np

points = np.empty((0, 3))
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
    x0, y0, w0 = 0, 0, 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 500:
            cv.drawContours(imgnew, cnt, -1, (255, 255 , 0), 3)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            print(area, peri, len(approx))
            x, y, w, h = cv.boundingRect(approx)
            x0 = x
            y0 = y
            w0 = w
            print(x, y, w)
            cv.rectangle(imgnew, (x, y), (x + w, y + h), (255, 0, 255), 5)
    return x0 + w0//2, y0



while True: 
    
    success, img = cap.read()
    img = cv2.circle(img, (140, 70), 6, (0, 255, 0), 2)
    img = cv2.circle(img, (190, 140), 6, (0, 0, 255), 2)
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

    points = np.vstack(points, np.array([x, y]))

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

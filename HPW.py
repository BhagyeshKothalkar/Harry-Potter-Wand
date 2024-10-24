import cv2 as cv
import numpy as np

letter = np.zeros((512, 512), dtype= np.uint8)
drawing = False
points = np.empty((0, 2), dtype=np.uint8)

cap = cv.VideoCapture(0)
cap.set(3, 512)
cap.set(4, 512)

def getContours(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 50:
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
    imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower = np.array([95, 155, 107])
    upper = np.array([105, 195 ,145])

    mask = cv.inRange(imgHSV, lower, upper)

    img_blur = cv.GaussianBlur(mask, (7, 7), 0)
    imgnew = cv.cvtColor(img_blur,cv.COLOR_GRAY2BGR)
    
    start_circle = np.array([[200, 50], [300, 50], [300, 150], [200, 150]])
    cv.rectangle(imgnew, start_circle[0], start_circle[2], (255, 255, 255), 3)
    end_circle = np.array([[200, 362], [300, 362], [300, 462], [200, 462]])
    cv.rectangle(imgnew, end_circle[0], end_circle[2], (255, 255, 255), 3)


    x, y = getContours(mask)
    print(x, y)

    if cv.pointPolygonTest(start_circle, np.array([x, y], dtype=np.float32), False)> 0:
        drawing = True
    if cv.pointPolygonTest(end_circle, np.array([x, y],dtype=np.float32), False)> 0 and drawing:
        drawing = False
        break

    if drawing:
        points = np.vstack((points, np.array([x, y])))
    
    for point in points:
        cv.circle(imgnew, point, 10, (255, 0, 0), cv.FILLED)
        cv.circle(letter, point, 10, (255), cv.FILLED)

    cv.imshow("img",cv.flip(imgnew, 1))
    cv.waitKey(2)

cv.destroyWindow('img')

letter = cv.resize(letter, np.array([28, 28], dtype = np.uint8))
letter = cv.flip(letter, 1)

cv.imshow('fin', letter)
cv.waitKey(0)

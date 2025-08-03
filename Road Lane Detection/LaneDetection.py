import cv2
import numpy as np


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def ROI(image):
    height = image.shape[0]
    triangle = np.array([[
        (200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, triangle, 255)
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image

def display_line(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            cv2.line(line_image, (x1,y1), (x2,y2), (255,0,0), 10)
    return line_image

def coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1=int((y1-intercept)/slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1,y1,x2,y2])


def average_slope(image, line): 
    left_fit=[]
    right_fit = []
    for line in lines:
        x1,y1,x2,y2=line.reshape(4)
        parameters= np.polyfit((x1,x2), (y1,y2), 1)
        print(parameters)
        slope=parameters[0]
        intercept=parameters[1]
        if slope<0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_avg = np.average(left_fit, axis=0)
    right_fit_avg = np.average(right_fit, axis=0)
    #left_line = coordinates(image, left_fit_avg)
    left_line = coordinates(image, left_fit_avg) if len(left_fit) > 0 else None
    right_line = coordinates(image, right_fit_avg) if len(right_fit) > 0 else None

    #right_line = coordinates(image, right_fit_avg)
    return np.array([left_line, right_line])



cap = cv2.VideoCapture("test2.mp4")
while (cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_image = ROI(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2,np.pi/100, 100, np.array([]), 40, 5)
    average_lines = average_slope(frame, lines)
    line_image = display_line(frame, average_lines)
    final_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow("Result", final_image)
    if cv2.waitKey(1) &0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

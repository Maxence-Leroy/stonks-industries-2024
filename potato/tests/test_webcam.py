import cv2
import math

def main():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    result, image = cam.read()
    if result:
        cv2.imshow("toto", image)
        cv2.waitKey(0)
        cv2.destroyWindow("toto") 
        detector_parameters = cv2.aruco.DetectorParameters()
        dictionnary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        detector = cv2.aruco.ArucoDetector(dictionary=dictionnary, detectorParams=detector_parameters)
        res = detector.detectMarkers(image)
        outputImage = image.copy()
        corners = res[0]
        first_marker_corners = corners[0][0]
        ids = res[1]
        print(first_marker_corners)
        x1 = first_marker_corners[0][0]
        y1 = first_marker_corners[0][1]
        x2 = first_marker_corners[1][0]
        y2 = first_marker_corners[1][1]
        angle = math.acos( (x2-x1) / math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2-y1, 2)))
        if y2 < y1:
            angle = -angle
        print(angle * 180 / math.pi)
        markers = cv2.aruco.drawDetectedMarkers(outputImage, corners, ids)
        cv2.imshow("toto", markers)
        cv2.waitKey(0)
        cv2.destroyWindow("toto") 

    else:
        print("Error")

if __name__ == "__main__":
    main()
import numpy as np
import cv2

def main():
    print("Start calibration")

    # Arrays to store object points and image points from all the images.
    obj_points: list[cv2.typing.MatLike] = [] # 3d point in real world space
    img_points: list[cv2.typing.MatLike] = [] # 2d points in image plane.

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    aruco_detector_parameters = cv2.aruco.DetectorParameters()
    aruco_dictionnary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
    aruco_detector = cv2.aruco.ArucoDetector(dictionary=aruco_dictionnary, detectorParams=aruco_detector_parameters)

    image_size: tuple[int, ...] = (0, 0, 0)

    for calibration_index in range(0, 10):
        right_calibration = False
        while not right_calibration:
            _ = input("Press when ready")
            result, image = cam.read()
            image_size = image.shape
            if not result:
                print("Could not capture image")
                continue

            marker_coordinates, marker_ids, _ = aruco_detector.detectMarkers(image)

            markers_expected_coordinates = [
                (20, (600, 1400)),
                (21, (2400, 1400)),
                (22, (600, 600)),
                (23, (600, 1400))
            ]

            objp = np.zeros((len(markers_expected_coordinates),3), np.float32)
            imgp = np.zeros((len(markers_expected_coordinates),2), np.float32)

            i = 0
            try:
                for marker in markers_expected_coordinates:
                    index = list(marker_ids).index(marker[0])
                    image_corners = marker_coordinates[index][0]
                    x1 = image_corners[0][0]
                    y1 = image_corners[0][1]
                    x2 = image_corners[2][0]
                    y2 = image_corners[2][1]
                    imgp[i] = [(x1 + x2) / 2, (y1 + y2) / 2]
                    objp[i] = [marker[1][0], marker[1][1], 0]
                    i += 1
                obj_points.append(objp)
                img_points.append(imgp)
                print(f"Calibration done {calibration_index + 1} / 10")
                right_calibration = True
                    
            except ValueError:
                print("Could not find tag " + str(i + 20))
                continue

    _, mtx, dist, _, _ = cv2.calibrateCamera(obj_points, img_points, [image_size[0], image_size[1]], np.zeros((0,0)), np.zeros((0,0)))
    print(mtx)
    print(dist)

if __name__ == "__main__":
    main()

"""
Res:

Camera Matrix: [[1.81655503e+03 0.00000000e+00 5.39500000e+02]
 [0.00000000e+00 4.55445722e+02 9.59500000e+02]
 [0.00000000e+00 0.00000000e+00 1.00000000e+00]]

Distortion: [-1.69386831e-11  5.11114896e-12 -7.84295642e-12 -5.78719914e-12]
"""
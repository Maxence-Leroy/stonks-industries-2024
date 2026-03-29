import cv2
import numpy as np
import time

def main():
    camera_matrix: cv2.typing.MatLike = np.array([[1.44201656e+03,0.00000000e+00,7.41332649e+02],
 [0.00000000e+00,1.75768411e+03,9.98958506e+02],
 [0.00000000e+00,0.00000000e+00,1.00000000e+00]], np.float32)
    distortion_coefficients: cv2.typing.MatLike = np.array([-0.27864588 , 0.42854672,  0.00647762, -0.06143282, -0.17472037], np.float32)

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    aruco_detector_parameters = cv2.aruco.DetectorParameters()
    aruco_dictionnary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
    aruco_detector = cv2.aruco.ArucoDetector(dictionary=aruco_dictionnary, detectorParams=aruco_detector_parameters)

    markers_expected_coordinates = [
        (20, (600, 1400)),
        (21, (2400, 1400)),
        (22, (600, 600)),
        (23, (2400, 600))
    ]

    objp = np.zeros((len(markers_expected_coordinates),3), np.float32)
    imgp = np.zeros((len(markers_expected_coordinates),2), np.float32)
    rvec: cv2.typing.MatLike = np.zeros((0,0))
    tvec: cv2.typing.MatLike = np.zeros((0,0))

    has_solved_pnp = False
    while not has_solved_pnp:
        result = True
        image = cv2.imread("/Users/maxence/Documents/Perso/stonks-industries-2024/potato/tests/image_test_for_pnp.png")
        #result, image = cam.read()
        if not result:
            print("Could not capture image")
            continue

        marker_coordinates, marker_ids, _ = aruco_detector.detectMarkers(image)

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
            print("PNP ready")
            has_solved_pnp, rvec, tvec = cv2.solvePnP(objp, imgp, camera_matrix, distortion_coefficients)
            if not has_solved_pnp:
                print("Could not solve PNP")
                time.sleep(2)

        except (ValueError, TypeError):
            print("Could not find tag " + str(i + 20))
            time.sleep(2)
            continue

    start_area: cv2.typing.MatLike = np.array([[0, 2000, 0], [600, 2000, 0], [600, 1550, 0], [0, 1550, 0]], np.float32)
    start = time.time()
    image_points, _ = cv2.projectPoints(start_area, rvec, tvec, camera_matrix, distortion_coefficients)
    end = time.time()
    print(end - start)
    result = False
    while not result:
        result = True
        image = cv2.imread("/Users/maxence/Documents/Perso/stonks-industries-2024/potato/tests/image_test_for_pnp.png")
        print(image_points)
        # result, image = cam.read()
        if result:
            for i in range(0, len(image_points)):
                current_point = point_to_cv(image_points[i][0])
                next_point = point_to_cv(image_points[(i + 1) % len(image_points)][0])

                image = cv2.line(image, current_point, next_point, (255, 0, 0), 5)
            cv2.imshow("toto", image)
            cv2.waitKey(0)
            cv2.destroyWindow("toto") 

def point_to_cv(point: cv2.typing.MatLike):
    x = min(max(0, int(point[0])), 1920)
    y = min(max(0, int(point[1])), 1080)
    return [x, y]
if __name__ == "__main__":
    main()
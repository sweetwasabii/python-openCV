from copy import deepcopy
from datetime import datetime as dt
from lab3 import Canny

import cv2
import numpy as np


def read_image(image_path, image_resolution):
    image = cv2.imread(image_path)
    image = cv2.resize(image, image_resolution)

    return image


def show_image(image, window_name):
    cv2.namedWindow(window_name, (450, 450))
    cv2.imshow(window_name, image)
    cv2.waitKey(0)


def show_images(images, window_names, x_shift, y_shift):
    index = 0
    x, y = 250, 0
    for image in images:
        cv2.namedWindow(window_names[index], cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow(window_names[index], x, y)
        cv2.imshow(window_names[index], image)

        index += 1

        if index % 2 != 0:
            y += y_shift
        else:
            x += x_shift
            y -= y_shift

    cv2.waitKey(0)


def add_time_to_image(image, time_ms, color=(255, 255, 255)):
    font = cv2.FONT_HERSHEY_PLAIN
    org = (10, 35)
    thickness = 2
    font_scale = 1.5

    cv2.putText(image, str(time_ms) + ' s', org, font, font_scale, color, thickness, cv2.LINE_AA)

    return image


def get_grayscale_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image


def get_blur_image(original_image, matrix_size, standard_deviation):
    grayscale_image = get_grayscale_image(original_image)
    blur_image = cv2.GaussianBlur(grayscale_image, (matrix_size, matrix_size), standard_deviation)

    return blur_image


def get_built_in_canny_image(image, th1, th2):
    canny_image = cv2.Canny(image, threshold1=th1, threshold2=th2)

    return canny_image


def get_canny_image(blur_image, image_resolution, operator_function):
    n, m = image_resolution
    gx, gy = operator_function(blur_image, image_resolution)

    matrix_length = np.zeros((n, m))  # значения градиентов
    matrix_atan = np.zeros((n, m))  # тангенсы (направления от 0 до 7)

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            x = int(gx[i][j])
            y = int(gy[i][j])
            matrix_length[i][j] = (x ** 2 + y ** 2) ** 0.5

            tg = -1
            if x != 0:
                tg = y / x

            value = -1

            if x > 0 and y < 0 and tg < -2.414 or \
                    x < 0 and y < 0 and tg > 2.414:
                value = 0
            elif x > 0 and y < 0 and tg < -0.414:
                value = 1
            elif x > 0 and y < 0 and tg > -0.414 or \
                    x > 0 and y > 0 and tg < 0.414:
                value = 2
            elif x > 0 and y > 0 and tg < 2.414:
                value = 3
            elif x > 0 and y > 0 and tg > 2.414 or \
                    x < 0 and y > 0 and tg < -2.414:
                value = 4
            elif x < 0 and y > 0 and tg < -0.414:
                value = 5
            elif x < 0 and y > 0 and tg > -0.414 or \
                    x < 0 and y < 0 and tg < 0.414:
                value = 6
            elif x < 0 and y < 0 and tg < 2.414:
                value = 7

            matrix_atan[i][j] = value

    low_level = 80
    high_level = 110

    matrix_border = deepcopy(blur_image)  # границы
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            way_plus = [[-1, -1], [-1, -1]]
            some = matrix_atan[i][j]
            # [y, x] logic
            if some == 0 or some == 4:
                way_plus = [[-1, 0], [1, 0]]
            elif some == 2 or some == 6:
                way_plus = [[0, -1], [0, 1]]
            elif some == 1 or some == 5:
                way_plus = [[-1, 1], [1, -1]]
            elif some == 3 or some == 7:
                way_plus = [[1, 1], [-1, -1]]

            grad = matrix_length[i][j]

            if grad >= matrix_length[i + way_plus[0][0]][j + way_plus[0][1]] \
                    and grad >= matrix_length[i + way_plus[1][0]][j + way_plus[1][1]]:
                matrix_border[i][j] = 0
            else:
                matrix_border[i][j] = 255

            if matrix_border[i][j] == 0:
                matrix_border[i][j] = 255
                subImg = matrix_border[i - 1:i + 2, j - 1:j + 2]
                min_el = np.min(subImg)

                if grad < low_level:
                    matrix_border[i][j] = 255
                elif grad > high_level:
                    matrix_border[i][j] = 0
                elif min_el == 0:
                    matrix_border[i][j] = 0

    return matrix_border


def get_sobel_image(blur_image):
    sobel_x = cv2.Sobel(blur_image, ddepth=cv2.CV_64F, dx=1, dy=0)
    sobel_y = cv2.Sobel(blur_image, ddepth=cv2.CV_64F, dx=0, dy=1)

    sobel_x = cv2.convertScaleAbs(sobel_x)
    sobel_y = cv2.convertScaleAbs(sobel_y)

    sobel_xy = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)

    return sobel_xy


def get_scharr_image(blur_image):
    scharr_x = cv2.Scharr(blur_image, cv2.CV_64F, 1, 0)
    scharr_y = cv2.Scharr(blur_image, cv2.CV_64F, 0, 1)

    scharr_x = cv2.convertScaleAbs(scharr_x)
    scharr_y = cv2.convertScaleAbs(scharr_y)

    scharr_xy = cv2.addWeighted(scharr_x, 0.5, scharr_y, 0.5, 0)

    return scharr_xy


def get_sobel(blur_image, image_resolution):
    n, m = image_resolution

    gx = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1],
    ])

    gy = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1],
    ])

    imgNew1 = np.zeros((n, m))
    imgNew2 = np.zeros((n, m))

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            subImg = blur_image[i - 1:i + 2, j - 1:j + 2]
            imgNew1[i][j] = np.sum(np.multiply(subImg, gx))
            imgNew2[i][j] = np.sum(np.multiply(subImg, gy))

    return imgNew1, imgNew2


def get_prewitt(blur_image, image_resolution):
    n, m = image_resolution

    gx = np.array([
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1],
    ])

    gy = np.array([
        [-1, -1, -1],
        [0, 0, 0],
        [1, 1, 1],
    ])

    imgNew1 = np.zeros((n, m))
    imgNew2 = np.zeros((n, m))

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            subImg = blur_image[i - 1:i + 2, j - 1:j + 2]
            imgNew1[i][j] = np.sum(np.multiply(subImg, gx))
            imgNew2[i][j] = np.sum(np.multiply(subImg, gy))

    return imgNew1, imgNew2


def get_scharr(blur_image, image_resolution):
    n, m = image_resolution

    gx = np.array([
        [3, 10, 3],
        [0, 0, 0],
        [-3, 10, -3],
    ])

    gy = np.array([
        [3, 0, -3],
        [10, 0, -10],
        [3, 0, -3],
    ])

    imgNew1 = np.zeros((n, m))
    imgNew2 = np.zeros((n, m))

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            subImg = blur_image[i - 1:i + 2, j - 1:j + 2]
            imgNew1[i][j] = np.sum(np.multiply(subImg, gx))
            imgNew2[i][j] = np.sum(np.multiply(subImg, gy))

    return imgNew1, imgNew2


def find_contours(blur_image, image_resolution):
    # get threshold image
    ret, thresh_image = cv2.threshold(blur_image, 130, 255, cv2.THRESH_BINARY)
    # return thresh_image

    # find contours
    contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # create an empty image for contours
    image_contours = np.uint8(np.zeros(image_resolution))

    cv2.drawContours(image_contours, contours, -1, (255, 255, 255), 1)

    return image_contours


def run_image(image_path='images/brain/insult.jpg', image_resolution=(450, 450)):
    original_image = read_image(image_path, image_resolution)

    my_canny = Canny()
    sobel = Canny.get_sobel
    prewitt = Canny.get_prewitt
    scharr = Canny.get_scharr

    kernel_size = (5, 5)
    deviation = 0
    thresholds = (130, 255)

    t0 = dt.now().second
    # 15 - макс
    blur_image = get_blur_image(original_image, kernel_size[0], deviation)

    t1 = dt.now().second
    # 80, 110 - супер
    # canny_image = get_built_in_canny_image(blur_image, 80, 110)
    # canny_by_sobel_image = get_canny_image(blur_image, image_resolution, get_sobel)
    canny_by_sobel_image = my_canny.get_canny_result(image_path, sobel, image_resolution, kernel_size, deviation,
                                                     thresholds)

    t2 = dt.now().second
    # sobel_image = get_sobel_image(blur_image)
    # canny_by_prewitt_image = get_canny_image(blur_image, image_resolution, get_prewitt)
    canny_by_prewitt_image = my_canny.get_canny_result(image_path, prewitt, image_resolution, kernel_size, deviation,
                                                       thresholds)

    t3 = dt.now().second
    # scharr_image = get_scharr_image(blur_image)
    # canny_by_scharr_image = get_canny_image(blur_image, image_resolution, get_scharr)
    canny_by_scharr_image = my_canny.get_canny_result(image_path, scharr, image_resolution, kernel_size, deviation,
                                                      thresholds)

    t4 = dt.now().second
    contours_image = find_contours(blur_image, image_resolution)

    t5 = dt.now().second

    blur_time = t1 - t0
    canny_by_sobel_time = t2 - t1
    canny_by_prewitt_time = t3 - t2
    canny_by_scharr_time = t4 - t3
    contours_time = t5 - t4

    images = [original_image, blur_image, canny_by_sobel_image, canny_by_prewitt_image, canny_by_scharr_image,
              contours_image]
    times = [blur_time, canny_by_sobel_time, canny_by_prewitt_time, canny_by_scharr_time, contours_time]

    images_time, index = [], 0
    for i in range(1, len(times) + 1):
        images_time.append(add_time_to_image(images[i], str(times[i - 1])))

    add_time_to_image(contours_image, contours_time, (255, 255, 255))

    images_time.insert(0, original_image)

    window_names = ['Original', 'Blur', 'Canny by Sobel', 'Canny by Prewitt', 'Canny by Sharr', 'findContours']

    x_shift, y_shift = image_resolution[0], image_resolution[1] + 30
    show_images(images_time, window_names, x_shift, y_shift)


def run_individual_task1():
    # 'evil_tumor.jpg'
    images_path = ['insult.jpg', 'multiple_sclerosis.jpg',
                   'metastases.jpg', 'evil_tumor2.jpg', 'good_brain.jpg']

    for i in range(len(images_path)):
        images_path[i] = 'images/brain/' + images_path[i]

    for image_path in images_path:
        run_image(image_path=image_path)


run_individual_task1()

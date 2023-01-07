import numpy as np
import cv2


class Canny:
    @staticmethod
    def read_image(image_path, image_resolution):
        image = cv2.imread(image_path)
        return cv2.resize(image, image_resolution)

    @staticmethod
    def get_grayscale_image(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def get_gaussian_blur(image, blur_size, deviation=0.0):
        return cv2.GaussianBlur(image, blur_size, deviation)

    @staticmethod
    def get_image_resolution(image):
        return image.shape[:2]

    @staticmethod
    def get_sobel(blur_image):
        n, m = blur_image.shape[:2]

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

        image_gx = np.zeros((n, m))
        image_gy = np.zeros((n, m))

        for i in range(1, n - 1):
            for j in range(1, m - 1):
                sub_image = blur_image[i - 1:i + 2, j - 1:j + 2]
                image_gx[i][j] = np.sum(np.multiply(sub_image, gx))
                image_gy[i][j] = np.sum(np.multiply(sub_image, gy))

        return image_gx, image_gy

    @staticmethod
    def get_prewitt(blur_image):
        n, m = blur_image.shape[:2]

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

        image_gx = np.zeros((n, m))
        image_gy = np.zeros((n, m))

        for i in range(1, n - 1):
            for j in range(1, m - 1):
                sub_image = blur_image[i - 1:i + 2, j - 1:j + 2]
                image_gx[i][j] = np.sum(np.multiply(sub_image, gx))
                image_gy[i][j] = np.sum(np.multiply(sub_image, gy))

        return image_gx, image_gy

    @staticmethod
    def get_scharr(blur_image):
        n, m = blur_image.shape[:2]

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

        image_gx = np.zeros((n, m))
        image_gy = np.zeros((n, m))

        for i in range(1, n - 1):
            for j in range(1, m - 1):
                sub_image = blur_image[i - 1:i + 2, j - 1:j + 2]
                image_gx[i][j] = np.sum(np.multiply(sub_image, gx))
                image_gy[i][j] = np.sum(np.multiply(sub_image, gy))

        return image_gx, image_gy

    @staticmethod
    def get_gradient_length(gx, gy):
        n, m = gx.shape[:2]
        gradient_length = np.zeros((n, m))

        for i in range(1, n - 1):
            for j in range(1, m - 1):
                x = int(gx[i][j])
                y = int(gy[i][j])
                gradient_length[i][j] = (x ** 2 + y ** 2) ** 0.5

        return gradient_length

    @staticmethod
    def get_gradient_direction(gx, gy):
        n, m = gx.shape[:2]
        gradient_direction = np.zeros((n, m))

        for i in range(1, n - 1):
            for j in range(1, m - 1):
                x = int(gx[i][j])
                y = int(gy[i][j])

                if x == 0:
                    gradient_direction[i][j] = 0
                    break
                elif y == 0:
                    gradient_direction[i][j] = 2
                    break

                tg = y / x

                if x > 0 and y < 0 and tg < -2.414 or \
                        x < 0 and y < 0 and tg > 2.414:
                    current_direction = 0
                elif x > 0 and y < 0 and tg < -0.414:
                    current_direction = 1
                elif x > 0 and y < 0 and tg > -0.414 or \
                        x > 0 and y > 0 and tg < 0.414:
                    current_direction = 2
                elif x > 0 and y > 0 and tg < 2.414:
                    current_direction = 3
                elif x > 0 and y > 0 and tg > 2.414 or \
                        x < 0 and y > 0 and tg < -2.414:
                    current_direction = 4
                elif x < 0 and y > 0 and tg < -0.414:
                    current_direction = 5
                elif x < 0 and y > 0 and tg > -0.414 or \
                        x < 0 and y < 0 and tg < 0.414:
                    current_direction = 6
                elif x < 0 and y < 0 and tg < 2.414:
                    current_direction = 7

                gradient_direction[i][j] = current_direction

        # print(gradient_direction)
        return gradient_direction

    @staticmethod
    def get_neighbors(gradient_direction):
        if gradient_direction == 0 or gradient_direction == 4:
            return [-1, 0], [1, 0]
        elif gradient_direction == 2 or gradient_direction == 6:
            return [0, -1], [0, 1]
        elif gradient_direction == 1 or gradient_direction == 5:
            return [-1, 1], [1, -1]
        elif gradient_direction == 3 or gradient_direction == 7:
            return [1, 1], [-1, -1]

    # границы - чёрные, фон - белый
    def get_suppression_of_non_maximums(self, gradient_length, gradient_direction):
        n, m = gradient_length.shape[:2]
        suppressed_matrix = np.zeros((n, m))

        for i in range(1, n - 1):
            for j in range(1, m - 1):
                neighbor1, neighbor2 = self.get_neighbors(gradient_direction[i][j])
                neighbor1_x, neighbor1_y = neighbor1
                neighbor2_x, neighbor2_y = neighbor2

                gradient = gradient_length[i][j]

                if gradient >= gradient_length[i + neighbor1_x][j + neighbor1_y] \
                        and gradient >= gradient_length[i + neighbor2_x][j + neighbor2_y]:
                    suppressed_matrix[i][j] = 255

        return suppressed_matrix

    @staticmethod
    def get_double_threshold_filtering(suppressed_matrix, gradient_length, thresholds):
        n, m = suppressed_matrix.shape[:2]

        # max_gradient_length = np.max(gradient_length)
        low_level, high_level = thresholds

        for i in range(1, n - 1):
            for j in range(1, m - 1):
                if suppressed_matrix[i][j] == 255:
                    suppressed_matrix[i][j] = 0
                    sub_image = suppressed_matrix[i - 1:i + 2, j - 1:j + 2]
                    max_element = np.max(sub_image)

                    if gradient_length[i][j] < low_level:
                        suppressed_matrix[i][j] = 0
                    elif gradient_length[i][j] > high_level:
                        suppressed_matrix[i][j] = 255
                    elif max_element == 255:
                        suppressed_matrix[i][j] = 255
                    # else:
                    #     print(sub_image, gradient_length[i][j], suppressed_matrix[i][j])
        return suppressed_matrix

    def get_canny_result(self, image_path, operator, image_resolution=(450, 450), blur_size=(5, 5), blur_deviation=0, thresholds=(20, 60)):
        image = self.read_image(image_path, image_resolution)

        grayscale_image = self.get_grayscale_image(image)
        # grayscale_image = cv2.imread(image_path, cv2.IMREAD_ANYDEPTH)
        blur_image = self.get_gaussian_blur(grayscale_image, blur_size, blur_deviation)

        gx, gy = operator(blur_image)

        gradient_length = self.get_gradient_length(gx, gy)
        gradient_direction = self.get_gradient_direction(gx, gy)

        non_maximus = self.get_suppression_of_non_maximums(gradient_length, gradient_direction)
        return self.get_double_threshold_filtering(non_maximus, gradient_length, thresholds)
        # double_threshold = self.get_double_threshold_filtering(non_maximus, gradient_length, thresholds)
        #
        # cv2.imshow('My Canny', double_threshold)
        # cv2.imshow('Built-in Canny', cv2.Canny(grayscale_image, 20, 60, apertureSize=3, L2gradient=True))
        #
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


canny_result = Canny()
canny_result.get_canny_result(r'images\LR3example.jpg', Canny.get_sobel, (604, 400))
# canny_result.get_canny_result(r'images\LR3example.jpg', Canny.get_prewitt)
# canny_result.get_canny_result(r'images\LR3example.jpg', Canny.get_scharr)

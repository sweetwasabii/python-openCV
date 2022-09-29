import cv2


class Lab1:
    @staticmethod
    def read_image(image_path):
        image = cv2.imread(image_path)
        window_name = 'Image Window'

        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(window_name, image)
        cv2.waitKey(0)

    @staticmethod
    def read_video(video_path, delay):
        video = cv2.VideoCapture(video_path, cv2.CAP_ANY)
        window_name = 'Video Window'

        is_frame_read, frame = video.read()
        previous_frame = frame

        while is_frame_read:
            cv2.imshow(window_name, frame)
            cv2.waitKey(delay)

            previous_frame = frame
            is_frame_read, frame = video.read()

        # самостоятельное закрытие окна
        cv2.imshow(window_name, previous_frame)
        cv2.waitKey(0)

        video.release()

    @staticmethod
    def read_and_save_ip_video(ip, output_video_name):
        video = cv2.VideoCapture(ip)
        window_name = 'IP Window'

        is_frame_read, frame = video.read()

        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(output_video_name, fourcc, 25, (width, height))

        while is_frame_read:
            cv2.imshow(window_name, frame)
            video_writer.write(frame)
            key = cv2.waitKey(1)

            # клавиша - escape
            if key == 27:
                break

            is_frame_read, frame = video.read()

        video.release()
        cv2.destroyAllWindows()

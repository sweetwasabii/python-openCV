import cv2
import numpy as np
import imutils
import datetime


def extract_car_numbers(video_path='video/car_numbers', video_name='cars2', video_extension='mp4', images_path='car_numbers'):
    cap = cv2.VideoCapture(f"{video_path}/{video_name}.{video_extension}")
    frame_number = int(cap.get(cv2.CAP_PROP_FPS))

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    cap_writer = cv2.VideoWriter(f"{video_path}/{video_name}_out.mp4v", fourcc, 25, (w, h))

    current_frame = 0
    while True:
        is_frame_read, frame = cap.read()
        current_frame += 1

        if not is_frame_read:
            break

        if current_frame % frame_number == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 30, 200)

            contours = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:8]

            pos = np.zeros(gray.shape, np.uint8)
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 10, True)

                if len(approx) == 4:
                    pos = approx
                    break

            if pos.any() != 0:
                # cv2.imshow('frame', frame)
                # cv2.waitKey(0)

                mask = np.zeros(gray.shape, np.uint8)
                contour = cv2.drawContours(mask, [pos], 0, 255, -1)
                # cv2.imshow('contour', contour)
                # cv2.waitKey(0)

                maskk = cv2.bitwise_and(frame, frame, mask=mask)
                # cv2.imshow('mask', maskk)
                # cv2.waitKey(0)

                (x, y) = np.where(mask == 255)
                (x1, y1) = (np.min(x), np.min(y))
                (x2, y2) = (np.max(x), np.max(y))

                # фото номера
                cropp = gray[x1:x2, y1:y2]
                # cv2.imshow('number', cropp)
                # cv2.waitKey(0)

                final_img = cv2.cvtColor(cv2.rectangle(frame, (y1, x1), (y2, x2), (0, 255, 0), 2), cv2.COLOR_BGR2RGB)
                cv2.putText(final_img, str(datetime.datetime.now()).split(' ')[1].split('.')[0], (w - 170, h - 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 8, cv2.LINE_AA)

                cv2.imshow('rectangle', final_img)

                cv2.imwrite(f'{images_path}/{video_name}_out_img_{current_frame}.jpg', cropp)
                cap_writer.write(final_img)

            key = cv2.waitKey(20)
            if key == 27:
                cap_writer.release()
                cap.release()
                break

    cap_writer.release()
    cap.release()
    cv2.destroyAllWindows()


extract_car_numbers('video/car_numbers', 'cars2', 'mp4')

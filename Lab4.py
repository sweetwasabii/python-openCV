from datetime import datetime
import cv2


def get_picture(path=r'images\LR3example.jpg'):
    return cv2.imread(path, cv2.IMREAD_ANYDEPTH)


def get_gaussian_blur(image, size=5, deviation=1.4):
    return cv2.GaussianBlur(image, (size, size), deviation)


def is_motion_frame(old_frame, new_frame):
    old_frame = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('old_frame', old_frame)

    new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('new_frame', new_frame)
    # cv2.waitKey(0)

    old_frame = cv2.GaussianBlur(old_frame, (5, 5), 1.3)
    # cv2.imshow('old_gb_frame', old_frame)

    new_frame = cv2.GaussianBlur(new_frame, (5, 5), 1.3)
    # cv2.imshow('new_gb_frame', new_frame)
    # cv2.waitKey(0)

    delta_frame = cv2.absdiff(old_frame, new_frame)
    # cv2.imshow('delta_frame', delta_frame)
    # cv2.waitKey(0)

    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow('thresh_frame', thresh_frame)
    # cv2.waitKey(0)

    contours, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 1000:
            return True


def get_motion_video(input_path, output_path):
    video = cv2.VideoCapture(input_path, cv2.CAP_ANY)
    is_frame_read, new_frame = video.read()

    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_path, fourcc, 25, (w, h))

    while is_frame_read:
        old_frame = new_frame
        is_frame_read, new_frame = video.read()

        if not is_frame_read:
            break

        if is_motion_frame(old_frame, new_frame):
            video_writer.write(new_frame)

    video.release()


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


def read_two_video(video_path1, video_path2):
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)

    while cap1.isOpened() or cap2.isOpened():
        is_frame_read1, frame1 = cap1.read()
        is_frame_read2, frame2 = cap2.read()

        if is_frame_read1:
            cv2.imshow('Original', frame1)

        if is_frame_read2:
            cv2.imshow('Motion', frame2)

        key = cv2.waitKey(15)

        # клавиша - escape
        if key == 27:
            break

    cap1.release()
    cap2.release()


def run_lab4():
    input_path = r'video\save\input2.mov'
    output_path = r'video\output_video.mov'

    get_motion_video(input_path, output_path)

    read_two_video(input_path, output_path)


run_lab4()

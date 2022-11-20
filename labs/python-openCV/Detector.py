from datetime import datetime
import cv2


def get_picture(path=r'images\LR3example.jpg'):
    return cv2.imread(path, cv2.IMREAD_ANYDEPTH)


def get_gaussian_blur(image, size=5, deviation=1.4):
    return cv2.GaussianBlur(image, (size, size), deviation)


def read_and_save_ip_video(ip, output_video_name):
    video = cv2.VideoCapture(ip)
    window_name = 'IP Window'

    is_frame_read, frame = video.read()

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_video_name, fourcc, 35, (width, height))

    font = cv2.FONT_HERSHEY_PLAIN
    color = (255, 255, 255)
    thickness = 2
    font_scale = 2
    org = (485, 40)

    while is_frame_read:
        time = str(datetime.now()).split(' ')[1].split('.')[0]
        frame = cv2.putText(frame, time, org, font,
                            font_scale, color, thickness, cv2.LINE_AA)

        cv2.imshow(window_name, frame)
        video_writer.write(frame)

        key = cv2.waitKey(1)

        # клавиша - escape
        if key == 27:
            break

        is_frame_read, frame = video.read()

    video.release()
    cv2.destroyAllWindows()


def is_motion_frame(old_frame, new_frame):
    old_frame = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)

    old_frame = cv2.GaussianBlur(old_frame, (5, 5), 1.3)
    new_frame = cv2.GaussianBlur(new_frame, (5, 5), 1.3)

    delta_frame = cv2.absdiff(old_frame, new_frame)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
    contours, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contours in contours:
        if cv2.contourArea(contours) > 1000:
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


def get_motion_video_from_ip(ip, input_path, output_path):
    input_video = cv2.VideoCapture(ip)
    output_video = cv2.VideoCapture(output_path, cv2.CAP_ANY)

    window_name = 'IP Window'

    width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    input_video_writer = cv2.VideoWriter(input_path, fourcc, 25, (width, height))
    output_video_writer = cv2.VideoWriter(output_path, fourcc, 25, (width, height))

    font = cv2.FONT_HERSHEY_PLAIN
    color = (255, 255, 255)
    org = (485, 40)
    thickness = 2
    font_scale = 2

    is_frame_read, new_frame = input_video.read()
    while is_frame_read:
        old_frame = new_frame
        is_frame_read, new_frame = input_video.read()

        if not is_frame_read:
            break

        time = str(datetime.now()).split(' ')[1].split('.')[0]
        frame = cv2.putText(new_frame, time, org, font,
                            font_scale, color, thickness, cv2.LINE_AA)

        cv2.imshow(window_name, new_frame)
        input_video_writer.write(new_frame)

        if is_motion_frame(old_frame, new_frame):
            output_video_writer.write(new_frame)

        key = cv2.waitKey(1)

        # клавиша - escape
        if key == 27:
            break

    input_video.release()
    output_video.release()

    cv2.destroyAllWindows()


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


def run_individual_task2():
    print('*** МЕНЮ ***:\n')
    print('1. Чтение уже записанного видео -> запись видео c движением;')
    print('2. Чтение видео с телефона -> запись видео c движением;')
    print('3. Чтение видео с телефона одновременное с записью видео c движением;\n')

    print('Выберите вариант >: ')
    variant = int(input())

    input_path = ''
    output_path = ''

    if variant == 1:
        input_path = r'video\input_video.mov'
        output_path = r'video\output_video.mov'

        get_motion_video(input_path, output_path)
    elif variant == 2:
        input_path = r'video\input_ip_video.mov'
        output_path = r'video\output_ip_video.mov'

        read_and_save_ip_video(1, input_path)
        get_motion_video(input_path, output_path)
    elif variant == 3:
        input_path = r'video\input_phone_video.mov'
        output_path = r'video\output_phone_video.mov'

        get_motion_video_from_ip(1, input_path, output_path)

    read_two_video(input_path, output_path)


run_individual_task2()

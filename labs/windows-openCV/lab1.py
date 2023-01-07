import cv2


class Lab1:
    @staticmethod
    def read_image(image_path):
        image = cv2.imread(image_path)
        window_name = 'Image Window'

        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(window_name, image)

        key = cv2.waitKey(0)

        # клавиша - escape
        if key == 27:
            cv2.destroyAllWindows()

    @staticmethod
    def read_video(video_path, delay):
        video = cv2.VideoCapture(video_path, cv2.CAP_ANY)
        window_name = 'Video Window'

        is_frame_read, frame = video.read()

        while is_frame_read:
            cv2.imshow(window_name, frame)
            cv2.waitKey(delay)

            is_frame_read, frame = video.read()

            key = cv2.waitKey(20)

            # клавиша - escape
            if key == 27:
                cv2.destroyAllWindows()
                break

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


def run_lab1_tasks():
    print('\n*** МЕНЮ ***\n')

    print('1) Показать изображение')
    print('2) Показать видео')
    print('3) Показать и записать видео с вебкамеры')
    print('4) Показать и записать видео с камеры телефона')
    print('5) Завершить програму\n')

    print('Выберите задание >: ')
    answer = input()

    if answer == '1':
        # print('\nВведите путь к файлу >: ')
        # path = input()

        Lab1.read_image(r'images\hello.jpg')
        run_lab1_tasks()
    elif answer == '2':
        # print('\nВведите путь к файлу >: ')
        # path = input()

        Lab1.read_video(r'video\main_video.mov', 5)
        run_lab1_tasks()
    elif answer == '3':
        # print('\nВведите название конечного файла >: ')
        # output_video_name = input()

        Lab1.read_and_save_ip_video(0, r"video\ip_laptop.mov")
        run_lab1_tasks()
    elif answer == '4':
        print('\nВКЛЮЧИТЕ IRIUN\n')

        # print('Введите название конечного файла >: ')
        # output_video_name = input()

        Lab1.read_and_save_ip_video(1, r'video\ip_phone.mov')
        run_lab1_tasks()
    elif answer == '5':
        return
    else:
        print('\n*** ПОПРОБУЙТЕ СНОВА ***')
        run_lab1_tasks()


run_lab1_tasks()

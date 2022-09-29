from Lab1 import Lab1 as Lab1


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
        print('\nВведите путь к файлу >: ')

        # C:\photo\f.JPG
        path = input()

        Lab1.read_image(path)
        run_lab1_tasks()
    elif answer == '2':
        print('\nВведите путь к файлу >: ')

        # C:\photo\test1.mp4
        path = input()

        Lab1.read_video(path, 5)
        run_lab1_tasks()
    elif answer == '3':
        print('\nВведите название конечного файла >: ')

        # windows_video.mov
        output_video_name = input()

        Lab1.read_and_save_ip_video(0, output_video_name)
        run_lab1_tasks()
    elif answer == '4':
        print('\nВКЛЮЧИТЕ IRIUN\n')

        print('Введите название конечного файла >: ')

        # phone_video.mov
        output_video_name = input()

        Lab1.read_and_save_ip_video(1, output_video_name)
        run_lab1_tasks()
    elif answer == '5':
        return
    else:
        print('\n*** ПОПРОБУЙТЕ СНОВА ***')
        run_lab1_tasks()


# 1) C:\photo\f.JPG
# 2) C:\photo\test1.mp4
# 3) video\windows_video.mov
# 4) video\phone_video.mov
run_lab1_tasks()

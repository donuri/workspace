import os
import cv2
from multiprocessing import Process


def find_video(root_path):
    for (path, dir, files) in os.walk(root_path):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.mp4':
                file_path = f'{path}\\{filename}'
                slice_video(file_path)
                # print(file_path)


def slice_video(video_path):
    vid_path_arr = video_path.split('\\')
    vidcap = cv2.VideoCapture(video_path)
    count = 0
    print(f'{vid_path_arr[-1]} start')
    while vidcap.isOpened():
        try:
            ret, image = vidcap.read()
            if ret and count % 10 == 0:
                print(f'{vid_path_arr[-1]}-{count}.png')
                # print(image)
                #cv2.imwrite(f'E:/seongwon/img/slice_images-2/{vid_path_arr[3]}/{vid_path_arr[-1][:-4]}-{count}.png', image)
                cv2.imwrite(f'C:/Users/jdnl/Documents/cache/slice_img-3/{vid_path_arr[-1][:-4]}-{count}.png', image)
                # print(f'E:/seongwon/img/{vid_path_arr[3]}/{vid_path_arr[4]}_img/{vid_path_arr[-1][:-4]}-{count}.mp4')

            elif ret == False:
                break

            count += 1

        except:
            break
    vidcap.release()


def main():
    p1 = Process(target=find_video, args=('E:\\seongwon\\img\\kim-2',))
    p2 = Process(target=find_video, args=('E:\\seongwon\\img\\lee-2',))
    p3 = Process(target=find_video, args=('E:\\seongwon\\img\\mun-2',))
    p4 = Process(target=find_video, args=('E:\\seongwon\\img\\jeong-2',))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

def main2():
    pt = Process(target=find_video, args=('C:\\Users\\jdnl\\Documents\\cache\\0313-3',))
    pt.start()
    pt.join()


if __name__ == '__main__':
    main2()
    # find_video('E:\\seongwon\\img\\kim')

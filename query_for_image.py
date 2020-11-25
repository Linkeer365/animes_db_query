import pymysql
import os
# from PIL import Image
import cv2
from PIL import Image

import sys


from io import BytesIO
import win32clipboard
from PIL import Image

# https://stackoverflow.com/questions/34322132/copy-image-to-clipboard

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def copy_img(img_path):
    out = BytesIO ()
    img_obj = Image.open (img_path)
    img_obj.convert ("RGB").save (out, "BMP")
    data = out.getvalue ()[14:]
    out.close ()
    send_to_clipboard (win32clipboard.CF_DIB, data)
    print ("copied!")


db_names='db_animes'
db=pymysql.connect('localhost','root','cc',db_names)
cursor=db.cursor()

quit=0

while not quit:
    query_anime=input("please input anime_name:")
    query_text=input("please input your text:")
    query_sql=f"select img from {query_anime} where text like '%{query_text}%'"

    try:
        cursor.execute(query_sql)
    except pymysql.err.ProgrammingError:
        print("数据表输错名字了！重来！")
        continue

    # print(cursor.fetchall())
    img_paths=[each[0] for each in cursor.fetchall()]

    if img_paths==[]:
        print("not fetched!")
        continue


    # print("img paths:",img_paths)

    cnt=1

    for img_path in img_paths:

        print(f"Img_idx:{cnt}; Left:{len(img_paths)-cnt}")

        # 键位对应

        esc_ord = 27
        enter_ord = 13

        # print('img path:',img_path)
        img=cv2.imread(img_path)

        # resize

        cv2.namedWindow ('kk', cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow ('kk', 100, 100)

        # width=12
        #
        # height=8

        width = 128
        height = int ((4 / 9) * width)
        scale = 5

        cube = (width * scale, height * scale)

        img = cv2.resize (img, cube, interpolation=cv2.INTER_CUBIC)

        res_fst = cv2.waitKey (1)

        iscopy=0


        while res_fst==-1:

            cv2.imshow('kk',img)
            res=cv2.waitKey(5000)

            if res==esc_ord:
                print("not copied!")
                break
            elif res==enter_ord:

                copy_img(img_path)

                iscopy=1

                quit=input("quit?[default not]")

                if quit=='y' or quit=='q':
                    sys.exit(0)
                else:
                    break
    quit = input ("one search done. quit?[default not]")
    if quit == 'y' or quit == 'q':
        sys.exit (0)
    else:
        continue

# print("one done.")



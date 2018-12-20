# -*- coding: utf-8 -*

import caffe
import lmdb
import numpy as np
import cv2
from caffe.proto import caffe_pb2

LMDB_FILE = '/your/path/to/lmdb_file'

def open_lmdb(lmdb_path):

    lmdb_env = lmdb.open(lmdb_path)

    lmdb_txn = lmdb_env.begin()  # 生成处理句柄
    lmdb_cursor = lmdb_txn.cursor()  # 生成迭代器指针
    annotated_datum = caffe_pb2.AnnotatedDatum()  # AnnotatedDatum结构

    return lmdb_cursor, annotated_datum

def check_annotation(lmdb_cursor, annotated_datum):

    for key, value in lmdb_cursor:
        print key

        annotated_datum.ParseFromString(value)
        datum = annotated_datum.datum  # Datum结构
        grps = annotated_datum.annotation_group  # AnnotationGroup结构
        type = annotated_datum.type

        image_x = np.fromstring(datum.data, dtype=np.uint8)  # 字符串转换为矩阵
        image = cv2.imdecode(image_x, -1)  # decode

        for grp in grps:

            for annotation in grp.annotation:
                xmin = annotation.bbox.xmin * datum.width  # Annotation结构
                ymin = annotation.bbox.ymin * datum.height
                xmax = annotation.bbox.xmax * datum.width
                ymax = annotation.bbox.ymax * datum.height

                print "bbox:", xmin, ymin, xmax, ymax  # object的bbox标签
                cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 1, cv2.LINE_AA)

            print "label:", grp.group_label  # object的name标签



        label = datum.label  # Datum结构label以及三个维度
        channels = datum.channels
        height = datum.height
        width = datum.width

        print "label:", label
        print "channels:", channels
        print "height:", height
        print "width:", width


        cv2.imshow("image", image)  # 显示图片
        wait_return = cv2.waitKey(0)

        if wait_return == ord("q"):
            cv2.destroyAllWindows()
            break


def run(lmbd_path):
    lmdb_cursor, annotated_datum = open_lmdb(lmbd_path)
    check_annotation(lmdb_cursor, annotated_datum)

if __name__ == "__main__":
    run(LMDB_FILE)

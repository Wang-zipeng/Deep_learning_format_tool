

import cv2
import os

from xml.dom.minidom import Document

xml_root = "your/path/store/xml/result"
yolo_root = "your/path/store/yolo/annotation_file"
image_root = "your/path/store/image_file"

def txt_To_xml():



    if not os.path.exists(xml_root):
        os.makedirs(xml_root)

    all_yoloannotation_path = os.listdir(yolo_root)

    for yolofile_path in all_yoloannotation_path:

        yolo_file = os.path.split(yolofile_path)[1]
        yolo_file_name = os.path.splitext(yolo_file)[0]

        xml_name = xml_root + yolo_file_name + '.xml'
        f = open(xml_name, "w")
        doc = Document()
        annotation = doc.createElement('annotation')
        doc.appendChild(annotation)

        folder = doc.createElement('folder')
        folder.appendChild(doc.createTextNode("img1"))
        annotation.appendChild(folder)

        filename = doc.createElement('filename')
        filename.appendChild(doc.createTextNode(yolo_file_name + '.jpg'))
        annotation.appendChild(filename)

        image = cv2.imread(os.path.join(image_root, yolo_file_name + ".jpg"))

        size = doc.createElement('size')
        width = doc.createElement('width')
        width.appendChild(doc.createTextNode(str(image.shape[1])))
        size.appendChild(width)
        height = doc.createElement('height')
        height.appendChild(doc.createTextNode(str(image.shape[0])))
        size.appendChild(height)
        depth = doc.createElement('depth')
        depth.appendChild(doc.createTextNode(str(image.shape[2])))
        size.appendChild(depth)
        annotation.appendChild(size)
        # data slice here
        datas = get_data_fromyolo(os.path.join(yolo_root, yolo_file_name + ".txt"), image.shape[1], image.shape[0])

        if len(datas) == 0:
            doc.writexml(f, indent='', addindent='\t', newl='\n', encoding='UTF-8')
            f.close()

        if os.path.exists(xml_name):
            os.remove(xml_name)

            continue


        for label_data in datas:
            annotation.appendChild(insertObject(doc, label_data))

        doc.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')

        f.close()

def get_data_fromyolo(yolo_path, width, height):


    datas = []
    f_handle = open(yolo_path)
    annotaiton_list = f_handle.readlines()

    for annotation in annotaiton_list:

        cur_datas = []

        label_list = annotation[:-1].split(",")
        cur_datas.append(int(label_list[1]))
        cur_datas.append(int(label_list[2]))
        cur_datas.append(int(label_list[1]) + int(label_list[3]))
        cur_datas.append(int(label_list[2]) + int(label_list[4]))

        if cur_datas[0] < 0:
            cur_datas[0] = 1

        if cur_datas[1] < 0:
            cur_datas[1] = 1

        if cur_datas[2] > width:
            cur_datas[2] = width - 1

        if cur_datas[3] > height:
            cur_datas[3] = height - 1


        class_label = int(label_list[0])

        if class_label == 1:
            cur_datas.append("pedestrain")
        elif class_label == 2:
            cur_datas.append("person_on_vehicle")
        elif class_label == 3:
            cur_datas.append("static_person")

        datas.append(cur_datas)


    return datas

def insertObject(doc, datas):
    obj = doc.createElement('object')

    name = doc.createElement('name')
    name.appendChild(doc.createTextNode(str(datas[4])))
    obj.appendChild(name)

    bndbox = doc.createElement('bndbox')

    xmin = doc.createElement('xmin')
    xmin.appendChild(doc.createTextNode(str(datas[0])))
    bndbox.appendChild(xmin)

    ymin = doc.createElement('ymin')
    ymin.appendChild(doc.createTextNode(str(datas[1])))
    bndbox.appendChild(ymin)

    xmax = doc.createElement('xmax')
    xmax.appendChild(doc.createTextNode(str(datas[2])))
    bndbox.appendChild(xmax)

    ymax = doc.createElement('ymax')
    ymax.appendChild(doc.createTextNode(str(datas[3])))
    bndbox.appendChild(ymax)

    obj.appendChild(bndbox)

    return obj


if __name__ == "__main__":
    txt_To_xml()
#!/usr/bin/env python
# -*- coding: utf8 -*-
import math
import codecs
from libs.constants import DEFAULT_ENCODING
import os


TXT_EXT = '.txt'
ENCODE_METHOD = DEFAULT_ENCODING


class RotatedYOLOWriter:

    def __init__(self, folder_name, filename, img_size, database_src='Unknown', local_img_path=None):
        self.folder_name = folder_name
        self.filename = filename
        self.database_src = database_src
        self.img_size = img_size
        self.box_list = []
        self.local_img_path = local_img_path
        self.verified = False

    def add_bnd_box(self, points, name, difficult, info = None):
        flat_points = []
        for x, y in points:
            flat_points.extend([x, y])
        # bndbox = {'points': flat_points, 'name': name, 'difficult': difficult}
        bndbox = {'points': flat_points, 'name': name, 'difficult': difficult, 'info': info}
        self.box_list.append(bndbox)

    # def save(self, target_file=None):
    #     out_file = None
    #     if target_file is None:
    #         out_file = codecs.open(
    #             self.filename + TXT_EXT, 'w', encoding=ENCODE_METHOD)
    #     else:
    #         out_file = codecs.open(target_file, 'w', encoding=ENCODE_METHOD)

    #     for box in self.box_list:
    #         x1, y1, x2, y2, x3, y3, x4, y4 = box['points']
    #         out_file.write("%.1f %.1f %.1f %.1f %.1f %.1f %.1f %.1f %s %s\n" % 
    #             (x1, y1, x2, y2, x3, y3, x4, y4, box['name'], box['difficult']))
    #     out_file.close()
    

    def bnd_box_to_yolo_line(self, box, class_list=[], info_items_list = None):

        # PR387
        box_name = box['name']
        if box_name not in class_list:
            class_list.append(box_name)

        class_index = class_list.index(box_name)

        # lấy info ra để lưu index của info
        info = box['info']
        staff_security_index = info_items_list[0].index(info[0])
        gender_index = info_items_list[1].index(info[1])
        age_index = info_items_list[2].index(info[2])
        QA_index = info_items_list[3].index(info[3])

        return class_index, \
            (staff_security_index, gender_index, age_index, QA_index)
    

    def save(self, target_file=None, class_list=[], info_items_list = None):
        out_file = None
        if target_file is None:
            out_file = codecs.open(
                self.filename + TXT_EXT, 'w', encoding=ENCODE_METHOD)
        else:
            out_file = codecs.open(target_file, 'w', encoding=ENCODE_METHOD)

        for box in self.box_list:
            x1, y1, x2, y2, x3, y3, x4, y4 = box['points']
            class_index, info = self.bnd_box_to_yolo_line(box, class_list, info_items_list = info_items_list)

            out_file.write("%d %.1f %.1f %.1f %.1f %.1f %.1f %.1f %.1f %d %d %d %d\n" % 
                (class_index, x1, y1, x2, y2, x3, y3, x4, y4, info[0], info[1], info[2], info[3]))
        out_file.close()


class RotatedYOLOReader:

    def __init__(self, file_path, info_items_list = None):
        self.shapes = []
        self.file_path = file_path
        self.verified = False

        # thinkman edit here
        class_list_path = None
        if class_list_path is None:
            dir_path = os.path.dirname(os.path.realpath(self.file_path))
            self.class_list_path = os.path.join(dir_path, "classes.txt")
        else:
            self.class_list_path = class_list_path

        # print (file_path, self.class_list_path)

        classes_file = open(self.class_list_path, 'r')
        self.classes = classes_file.read().strip('\n').split('\n')

        # từ index để lấy được thông tin info của detection
        self.info_items_list = info_items_list

        self.parse_rotated_yolo_format()

    def get_shapes(self):
        return self.shapes

    def get_angle(self, x1, y1, x2, y2):
        return math.atan2(y2 - y1, x2 - x1)
    
    # def add_shape(self, x1, y1, x2, y2, x3, y3, x4, y4, label, difficult):
    #     angle = self.get_angle(x1, y1, x2, y2)
    #     points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    #     self.shapes.append((label, points, None, None, difficult, angle))

    def add_shape(self, x1, y1, x2, y2, x3, y3, x4, y4, label, info, difficult):
        angle = self.get_angle(x1, y1, x2, y2)
        points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

        self.shapes.append((label, info, points, None, None, difficult, angle))

    def yolo_line_to_shape(self, class_index, info_index_list):
        label = self.classes[int(class_index)]
        info = [self.info_items_list[i][int(info_index_list[i])] for i in range(len(self.info_items_list))]

        return label, info

    def parse_rotated_yolo_format(self):
        bnd_box_file = open(self.file_path, 'r')
        for bndBox in bnd_box_file:
            # x1, y1, x2, y2, x3, y3, x4, y4, label, difficult = bndBox.strip().split(' ')
            # self.add_shape(float(x1), float(y1), float(x2), float(y2), float(x3), float(y3),
            #     float(x4), float(y4), label, int(difficult))
            class_index, x1, y1, x2, y2, x3, y3, x4, y4, *info_index_list = bndBox.strip().split(' ')
            
            label, info = self.yolo_line_to_shape(class_index, info_index_list)
            
            self.add_shape(float(x1), float(y1), float(x2), float(y2), float(x3), float(y3),
                float(x4), float(y4), label, info, False)

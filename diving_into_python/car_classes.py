# -*- coding: utf-8 -*-
import os
import csv
import re


class CarBase():
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = str(brand)
        self.photo_file_name = str(photo_file_name)
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[-1]


class Car(CarBase):
    # list attributes for this type of cars
    validation_list = "brand", "photo_file_name", "carrying", "passenger_seats_count"

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = str("car")
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    validation_list = "brand", "photo_file_name", "carrying", "body_whl"

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = str("truck")
        self._set_size(body_whl)

    def _set_size(self, whl):
        length, width, height = [0] * 3
        val = re.findall(r'^(\d+\.?\d+|\d+)x(\d+\.?\d+|\d+)x(\d+\.?\d+|\d+)$', str(whl))
        if val:
            length, width, height = list(val[0])
        self.body_length = float(length)
        self.body_width = float(width)
        self.body_height = float(height)

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    validation_list = "brand", "photo_file_name", "carrying", "extra"

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = "spec_machine"


def photo_file_test(path):
    find = re.findall(r"\w+\.(?:jpg|jpeg|png|gif)$", path)
    if find:
        return str(path)
    else:
        raise ValueError


def non_empty_str_test(path):
    find = re.findall(r"\w+", str(path))
    if find:
        return str(path)
    else:
        raise ValueError


# test csv string, and convert it to nessesery type
def convert_data(validation_list, dic):
    # get nessesery attributes from line
    dic = {x: dic[x] for x in validation_list}
    fanc = {"brand": non_empty_str_test,
            "passenger_seats_count": int,
            "photo_file_name": photo_file_test,
            "carrying": float,
            "body_whl": str,
            "extra": non_empty_str_test}
    for key in dic.keys():
        try:
            dic[key] = fanc[key](dic[key])
        except ValueError:
            return None
    return dic.values()


def get_car_list(csv_filename):
    with open(csv_filename) as csv_fd:
        # csv filename object:
        reader = csv.reader(csv_fd, delimiter=';')
        # get first line of csv
        keys = next(reader)
        obj_list = []
        for row in reader:
            dic = dict(zip(keys, row))
            try:
                if dic['car_type'] == 'car':
                    atr = convert_data(Car.validation_list, dic)
                    if atr:
                        obj_list.append(Car(*atr))
                elif dic['car_type'] == "truck":
                    atr = convert_data(Truck.validation_list, dic)
                    if atr:
                        obj_list.append(Truck(*atr))
                elif dic['car_type'] == "spec_machine":
                    atr = convert_data(SpecMachine.validation_list, dic)
                    if atr:
                        obj_list.append(SpecMachine(*atr))
            except KeyError:
                pass
    return obj_list
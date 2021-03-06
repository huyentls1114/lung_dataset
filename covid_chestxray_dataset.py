import os
import glob
import shutil
import numpy as np
import random
import tqdm

class CovidChestXray:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

        self.init_name()
        self.init_output()

        self.list_img_name = None

    def init_name(self):
        self.image_folder = os.path.join(self.input_folder, "images")
        self.mask_folder = os.path.join(self.input_folder, "annotations/lungVAE-masks")
        self.list_mask_names = os.listdir(self.mask_folder)
    def init_output(self):
        self.output_image_folder = os.path.join(self.output_folder, "images")
        self.output_mask_folder = os.path.join(self.output_folder, "masks")
        if not os.path.isdir(self.output_image_folder):
            os.makedirs(self.output_image_folder)
        if not os.path.isdir(self.output_mask_folder):
            os.makedirs(self.output_mask_folder)

    def copy_images(self):
        self.list_img_name = []
        for mask_name in self.list_mask_names:
            try:
                img_path = glob.glob(self.image_folder+os.sep+mask_name.replace("_mask.png", "*").replace(".png", ""))[0]
                img_name = img_path.split(os.sep)[-1]
                mask_path = os.path.join(self.mask_folder, mask_name)
                img_path_output = os.path.join(self.output_image_folder, img_name)
                mask_path_output = os.path.join(self.output_mask_folder, img_name)
                shutil.copy(img_path, img_path_output)
                shutil.copy(mask_path, mask_path_output)
                self.list_img_name.append(img_name)
            except Exception as e:
                print(mask_name)
                print(e)

    def split_train_val(self, train_rate):
        if self.list_img_name is None:
            self.list_img_name = os.listdir(self.output_image_folder)
        assert len(self.list_img_name) >0
        list_index = np.array(range(len(self.list_img_name)))
        random.shuffle(list_index)

        list_train  = np.array(list_index[:int(len(list_index)*train_rate)])
        list_valid = np.array(list_index[int(len(list_index)*train_rate):])
        self.list_img_name = np.array(self.list_img_name)
        self.dict_img_name = {
            "train": self.list_img_name[list_train],
            "valid": self.list_img_name[list_valid]
        }

    def save_txt(self, mode="train"):
        file_path = os.path.join(self.output_folder, "%s.txt" % mode)
        if os.path.isfile(file_path):
            os.remove(file_path)
        file_ = open(file_path, "w")
        for img_name in self.dict_img_name[mode]:
            file_.writelines(img_name+"\n")
        file_.close()

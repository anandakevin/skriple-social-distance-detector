# %cd '/mnt/e/Projects/Skripsi - AI - Social Distancing Detector/Datasets/RAiD Dataset-master'
# %cd '/mnt/e/Projects/Skripsi - AI - Social Distancing Detector/Datasets/car_devkits'

from scipy.io import loadmat
import pandas as pd
# annots = loadmat('example_v7.mat')
annots = loadmat('E:\Projects\Skripsi - AI - Social Distancing Detector\Datasets\car_devkits\cars_train_annos.mat')
# annots = loadmat('cars_test_annos.mat')
# annots = loadmat('cars_meta.mat')
annots.keys()

annots["annotations"][0][0]["bbox_x1"], annots["annotations"][0][0]["fname"]

# print(annots["annotations"][0][0])

# print ([item.flat[0] for item in annots["annotations"][0][0]])

# for item in annots["annotations"][0]:
#     # print(item)
#     print ([item])
#     print ([item.flat[0]])

data = [[row.flat[0] for row in line] for line in annots["annotations"][0]]
columns = ["bbox_x1", "bbox_y1", "bbox_x2", "bbox_y2", "class", "fname"]
df_train = pd.DataFrame(data, columns=columns)

print(df_train)
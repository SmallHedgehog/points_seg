from __future__ import print_function
from __future__ import absolute_import

import torch.utils.data as data
import torch
import numpy as np
from dataset.vis  import draw_lidar_simple
import mayavi.mlab as mlab


class LidarDataset(data.Dataset):
    def __init__(self, npoints = 4096, split = 'train'):
        self.npoints = npoints
        self.split = split
        self.pathfile = ''
        self.pathlist = []

        # load paths file
        if self.split == 'train:':
            self.pathfile = '../data/example.txt'
        elif self.split == 'val':
            self.pathfile = '../data/example.txt'
        else:
            self.pathfile = '../data/example.txt'

        # read file paths
        with open(self.pathfile) as f:
            for line in f.readlines():
                self.pathlist.append(line.rstrip('\n'))


    def __getitem__(self, index):
        # laad data
        path = self.pathlist[index]
        data = np.load(path)

        # resample
        choice = np.random.choice(len(data), self.npoints, replace=True)

        # if test, only return points
        points = data[choice, 0:4]
        if self.split == 'test':
            return points

        # if train/val, return points and labels
        labels = data[choice, 4]
        return points, labels


    def __len__(self):
        return len(self.pathlist)



if __name__ == '__main__':
    pointset = LidarDataset(npoints = 8192, split = 'train')
    pointloader = data.DataLoader(pointset, batch_size=1, num_workers=0, shuffle=False)
    for index, (points, labels) in enumerate(pointloader):
        print (index, points.shape, labels.shape)
        p1 = points.numpy()
        p2 = labels.numpy()
        # p1 = np.squeeze(p1, 0)
        # p2 = np.squeeze(p2, 0)
        # fig = draw_lidar_simple(p1, p2)
        # raw_input()
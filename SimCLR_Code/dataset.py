import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import torch.optim as optim 
import torch
from torch.utils.data import TensorDataset, DataLoader
from pytorch_metric_learning.losses import NTXentLoss
import torchvision.transforms as transforms
from typing import Optional
from pytorch_lightning import LightningDataModule
import h5py

class Galaxy10_Dataset(LightningDataModule):
    def __init__(self,datadir,batch_size = 32):
        super(Galaxy10_Dataset).__init__()
        self.file_path = datadir
        self.batch_size = batch_size

    def prepare_data(self):
        pass

    def setup(self, stage = None):
        with h5py.File(self.file_path, 'r') as F:
            images = np.array(F['images'])
            labels = np.array(F['ans'])
        
        labels = np.eye(10)[labels]
        labels = labels.astype(np.float32)
        images = images.astype(np.float32)
        images = images/255
        images = images.transpose((0,3,1,2))

        images = torch.from_numpy(images)
        labels = torch.from_numpy(labels)
        X_train, X_test, y_train, y_test = train_test_split(images,labels, test_size = 0.2)
        X_valid, X_test, y_valid, y_test = train_test_split(X_test,y_test, test_size = 0.5)

        self.train = TensorDataset(X_train,y_train)
        self.valid = TensorDataset(X_valid,y_valid)
        self.test = TensorDataset(X_test,y_test)
    
    def train_dataloader(self):
        return DataLoader(self.train, batch_size = 32, shuffle=True)
    
    def val_dataloader(self):
        return DataLoader(self.valid, batch_size = 32, shuffle=True)
    
    def test_dataloader(self):
        return DataLoader(self.test, batch_size = 32, shuffle=True)
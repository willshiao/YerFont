import argparse
import os
import numpy as np
import math

import torchvision.transforms as transforms
from torchvision.utils import save_image
from PIL import Image

from torchvision import datasets
from torchvision import datasets as dsets
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
from skimage import io

import torch.nn as nn
import torch.nn.functional as F
import torch
from os import path
import glob

os.makedirs("images", exist_ok=True)

parser = argparse.ArgumentParser()
parser.add_argument("--n_epochs", type=int, default=200, help="number of epochs of training")
parser.add_argument("--batch_size", type=int, default=64, help="size of the batches")
parser.add_argument("--lr", type=float, default=0.0002, help="adam: learning rate")
parser.add_argument("--b1", type=float, default=0.5, help="adam: decay of first order momentum of gradient")
parser.add_argument("--b2", type=float, default=0.999, help="adam: decay of first order momentum of gradient")
parser.add_argument("--n_cpu", type=int, default=8, help="number of cpu threads to use during batch generation")
parser.add_argument("--latent_dim", type=int, default=100, help="dimensionality of the latent space")
parser.add_argument("--n_classes", type=int, default=10, help="number of classes for dataset")
parser.add_argument("--img_size", type=int, default=32, help="size of each image dimension")
parser.add_argument("--channels", type=int, default=1, help="number of image channels")
parser.add_argument("--sample_interval", type=int, default=400, help="interval between image sampling")
opt = parser.parse_args()
print(opt)

img_shape = (opt.channels, opt.img_size, opt.img_size)

cuda = True if torch.cuda.is_available() else False


class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()

        self.label_emb = nn.Embedding(opt.n_classes, opt.n_classes)

        def block(in_feat, out_feat, normalize=True):
            layers = [nn.Linear(in_feat, out_feat)]
            if normalize:
                layers.append(nn.BatchNorm1d(out_feat, 0.8))
            layers.append(nn.LeakyReLU(0.2, inplace=True))
            return layers

        self.model = nn.Sequential(
            *block(opt.latent_dim + opt.n_classes, 128, normalize=False),
            *block(128, 256),
            *block(256, 512),
            *block(512, 1024),
            nn.Linear(1024, int(np.prod(img_shape))),
            nn.Tanh()
        )

    def forward(self, noise, labels):
        # Concatenate label embedding and image to produce input
        gen_input = torch.cat((self.label_emb(labels), noise), -1)
        img = self.model(gen_input)
        img = img.view(img.size(0), *img_shape)
        return img


class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()

        self.label_embedding = nn.Embedding(opt.n_classes, opt.n_classes)

        self.model = nn.Sequential(
            nn.Linear(opt.n_classes + int(np.prod(img_shape)), 512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 512),
            nn.Dropout(0.4),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 512),
            nn.Dropout(0.4),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 1),
        )

    def forward(self, img, labels):
        # Concatenate label embedding and image to produce input
        d_in = torch.cat((img.view(img.size(0), -1), self.label_embedding(labels)), -1)
        validity = self.model(d_in)
        return validity


# Loss functions
adversarial_loss = torch.nn.MSELoss()

# Initialize generator and discriminator
generator = Generator()
discriminator = Discriminator()

if cuda:
    generator.cuda()
    discriminator.cuda()
    adversarial_loss.cuda()

# Configure data loader
transform = transforms.Compose([
    transforms.Resize((opt.img_size, opt.img_size), Image.BICUBIC),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,)),
])

emnist_dset = dsets.EMNIST(
    root='../../data',
    train=True,
    split='letters',
    transform=transform,
    download=False
)
class LetterDataset(Dataset):
    def __init__(self, root_dir='../../data', trans=None, letters=list('abcdefghijklmnopqrstuvwxyz')):
        self.ltr_map = {}
        self.letters = letters
        for ltr in letters:
            self.ltr_map[ltr] = len(glob.glob(path.join(root_dir, f'{ltr}_imgs', '*.png')))
        self.sfx_arr = []
        total = 0
        for ltr in letters:
            total += self.ltr_map[ltr]
            self.sfx_arr.append(total)
        self.total_size = total
        self.transform = trans
        self.root_dir = root_dir
    
    def __len__(self):
        return self.total_size

    def __getitem__(self, idx):
#         print('sfx: ', self.sfx_arr)
#         print('idx: ', idx)
#         offset = None
        for i, bound in enumerate(self.sfx_arr):
            if idx < bound:
#                 print('idx < bound')
                ltr_idx = i
                curr_ltr = self.letters[i]
#                 print('i=', i)
                if i == 0:
                    offset = 0
                else:
                    offset = self.sfx_arr[i - 1]
                break
        diff = idx-offset
        sample = Image.open(path.join(self.root_dir, f'{curr_ltr}_imgs', f'{curr_ltr}_img_{diff}.png'))
#         print('current letter:', curr_ltr)
        if self.transform:
            sample = self.transform(sample)
        return (sample, ltr_idx)

# for a in emnist_dset:
# print(emnist_dset)
#     break

ltr_dset = LetterDataset(trans=transform)

# print(ltr_dset[0][0].shape, len(ltr_dset))
# print(emnist_dset[0][0].shape, 'len is', len(emnist_dset))

# print(emnist_dset[0])
dataloader = torch.utils.data.DataLoader(dataset=ltr_dset,
    batch_size=opt.batch_size,
    shuffle=True
)

# Optimizers
optimizer_G = torch.optim.Adam(generator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2))
optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2))

FloatTensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor
LongTensor = torch.cuda.LongTensor if cuda else torch.LongTensor


def sample_image(n_row, batches_done):
    """Saves a grid of generated digits ranging from 0 to n_classes"""
    # Sample noise
    z = Variable(FloatTensor(np.random.normal(0, 1, (n_row ** 2, opt.latent_dim))))
    # Get labels ranging from 0 to n_classes for n rows
    labels = np.array([num for _ in range(n_row) for num in range(n_row)])
    labels = Variable(LongTensor(labels))
    gen_imgs = generator(z, labels)
    save_image(gen_imgs.data, "images/%d.png" % batches_done, nrow=n_row, normalize=True)

from torchvision import transforms

# ----------
#  Training
# ----------
generator.load_state_dict(torch.load('models/generator.pt'))
discriminator.load_state_dict(torch.load('models/discriminator.pt'))
alphabet = 'abcdefghijklmnopqrstuvwxyz'
generator.eval()
for i in range((opt.n_classes)):
    z = Variable(FloatTensor(np.random.normal(0, 1, (opt.batch_size, opt.latent_dim))))
    gen_labels = Variable(LongTensor(np.ones((opt.batch_size,)) * i))
    gen_imgs = generator(z, gen_labels)
    gen_imgs_cpu = gen_imgs.detach().cpu()
    sub_path = path.join('gen', alphabet[i])
    os.makedirs(sub_path, exist_ok=True)
    for j in range(opt.batch_size):
        converted = transforms.ToPILImage()(gen_imgs_cpu[j, :, :])
        converted.save(path.join(sub_path, f'img_{j}.png'))
#     print(converted)
    

#         print('Labels:', gen_labels)
        # Generate a batch of images

# z = Variable(FloatTensor(np.random.normal(0, 1, (opt.batch_size, opt.latent_dim))))
# labels = Variable(torch.zeros((opt.batch_size,)).type(LongTensor))
# generator.eval()
# gen_imgs = generator(z, labels)
# save_image(gen_imgs.data, "images/done.png", nrow=5, normalize=True)
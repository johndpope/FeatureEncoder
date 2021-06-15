from argparse import Namespace
import time
import os
import sys
import pprint
import numpy as np
from PIL import Image
import logging
import torch
import torchvision.transforms as transforms
from utils.common import tensor2im
from models.psp import pSp
from utils.inference_utils import run_on_batch
import matplotlib.pyplot as plt
import os


DATA = {
    "model_path": "/home/jovyan/FeatureEncoder/pretrained_models/restyle_psp_ffhq_encode.pt",
    "image_path": "notebooks/images/face_img.jpg"
}


model_path = DATA["model_path"]

# step 4 load pretrained model
ckpt = torch.load(model_path, map_location='cpu')

opts = ckpt['opts']

# update the training options
opts['checkpoint_path'] = model_path

opts = Namespace(**opts)
net = pSp(opts)

net.eval()
net.cuda()

def run(image_path):
    # step 5
    
    original_image = Image.open(image_path).convert("RGB")
    
    input_image = original_image.resize((256, 256))
    
    # todo print image


    # step 6

    img_transforms = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
        
    transformed_image = img_transforms(input_image)

    def get_avg_image(net):
        avg_image = net(net.latent_avg.unsqueeze(0),
                        input_code=True,
                        randomize_noise=False,
                        return_latents=False,
                        average_code=True)[0]
        avg_image = avg_image.to('cuda').float().detach()

        return avg_image
    
    opts.n_iters_per_batch = 1
    opts.resize_outputs = False  # generate outputs at full resolution

    with torch.no_grad():
        avg_image = get_avg_image(net)
        tic = time.time()
        result_batch, result_latents = run_on_batch(transformed_image.unsqueeze(0).cuda(), net, opts, avg_image)
        toc = time.time()
        #print('Inference took {:.4f} seconds.'.format(toc - tic))
    
    return result_latents

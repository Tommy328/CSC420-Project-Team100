import os
import sys
import time
import pathlib
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import random
import numpy as np
import matplotlib.pyplot as plt

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--path', type=str, help='Path to the log file')
parser.add_argument('--output', type=str, help='path to the output directory')

def loss_plots(path, output):
    count = 0
    psnr = []
    mae = []
    step = 1000
    with open(path, 'r') as f:
        p = []
        m = []
        for line in f:
            if count % step < step:
                pi, mi = line.split(" ")[-2:]
                p.append(float(pi))
                m.append(float(mi))
            if count % step == step-1:
                psnr.append(np.mean(p))
                mae.append(np.mean(m))
                p = []
                m = []
            count += 1

    iters = np.arange(0, 20000, step)
    fig1 = plt.figure()
    plt.plot(iters, psnr)
    plt.xlabel("iteration")
    plt.ylabel("PSNR")
    plt.xticks(np.arange(0, 20001, step*2.5))
    fig1.savefig(output + "psnr.png")

    fig2 = plt.figure()
    plt.plot(iters, mae)
    plt.xlabel("iteration")
    plt.ylabel("MAE")
    plt.xticks(np.arange(0, 20001, step*2.5))
    fig2.savefig(output + "mae.png")

if __name__ == '__main__':
    args = parser.parse_args()
    loss_plots(args.path, args.output)

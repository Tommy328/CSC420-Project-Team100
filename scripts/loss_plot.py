import os
import glob
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import numpy as np
import matplotlib.pyplot as plt

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--path', type=str, help='Path to the log file', required=False)
parser.add_argument('--output', type=str, help='Path to the output directory', required=False)
parser.add_argument('--dir', type=str, help='Path to the model checkpoints directory, automatically find .dat file. '
                                            'Output will also be saved here', required=False)


def mae_psnr_plots(path, output, train=True):
    # PLOT MAE AND PSNR: this is only for inpainting/gradients. Use recall/precision for edges
    # If plotting training logs, train = True
    count = 0
    psnr = []
    mae = []
    step = 100
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

    iters = np.arange(step, 200001, step*10)
    fig1 = plt.figure()
    plt.plot(iters, psnr)
    plt.xlabel("iteration")
    plt.ylabel("PSNR")
    plt.xticks(np.arange(0, 200001, 50000))
    if train:
        plt.title('PSNR during training')
    fig1.savefig(os.path.join(output, "psnr.png"))

    fig2 = plt.figure()
    plt.plot(iters, mae)
    plt.xlabel("iteration")
    plt.ylabel("MAE")
    plt.xticks(np.arange(0, 200001, 50000))
    if train:
        plt.title('MAE during training')
    fig2.savefig(os.path.join(output,"mae.png"))


def precision_recall_plots(path, output, train=True):
    # only used for edge generation model
    count = 0
    precision = []
    recall = []
    step = 100
    with open(path, 'r') as f:
        p = []
        r = []
        for line in f:
            if count % step < step:
                pi, ri = line.split(" ")[-2:]
                p.append(float(pi))
                r.append(float(ri))
            if count % step == step-1:
                precision.append(np.mean(p))
                recall.append(np.mean(r))
                p = []
                r = []
            count += 1

    iters = np.arange(step, 200001, step*10)
    fig1 = plt.figure()
    plt.plot(iters, precision)
    plt.xlabel("iteration")
    plt.ylabel("Precision")
    plt.xticks(np.arange(0, 200001, 50000))
    if train:
        plt.title('Precision during training')
    fig1.savefig(os.path.join(output, "precision.png"))

    fig2 = plt.figure()
    plt.plot(iters, recall)
    plt.xlabel("iteration")
    plt.ylabel("Recall")
    plt.xticks(np.arange(0, 200001, 50000))
    if train:
        plt.title('Recall during training')
    fig2.savefig(os.path.join(output,"recall.png"))


def loss_plots(path, output, loss_items):
    # plot n graphs for n types of losses in loss_items
    count = 0
    n = len(loss_items)
    loss = [[] for i in range(n)]
    step = 100

    with open(path, 'r') as f:
        l = np.zeros((n, step))
        for line in f:
            if len(line.split(" ")[2:]) != n + 2:
                raise Exception('Incorrect number of loss items!')
            if count % step < step:
                losses = line.split(" ")[2:]
                for i in range(n):
                    l[i, count % step] = float(losses[i])
            if count % step == step-1:
                for i in range(n):
                    loss[i].append(np.mean(l[i]))
                l = np.zeros((n, step))
            count += 1

    iters = np.arange(step, 200001, step*10)
    for i in range(n):
        fig = plt.figure()
        plt.plot(iters, loss[i])
        plt.xlabel("iteration")
        plt.ylabel(loss_items[i])
        plt.xticks(np.arange(0, 200001, 50000))
        plt.title(f'{loss_items[i]} during training')
        fig.savefig(os.path.join(output,f"{loss_items[i]}.png"))


if __name__ == '__main__':
    args = parser.parse_args()

    if args.dir:
        output = args.dir
        path = glob.glob(os.path.join(output, '*.dat'))[0]
    else:
        output = args.output
        path = args.path

    # for edge/gradient model, with 3 losses in log:
    #loss_plots(path, output, ['disc_loss', 'gen_adversarial_loss', 'gen_feature_matching_loss'])
    #precision_recall_plots(path,output) # if edge generator
    # mae_psnr_plots(path, output)   # if gradient generator

    # for inpaint model, with 4 losses in log:
    loss_plots(args.path, args.output, ['disc_loss', 'gen_adversarial_loss', 'gen_L1_loss', 'gen_perceptual_loss', 'gen_style_loss'])
    # mae_psnr_plots(path, output)


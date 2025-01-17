## CSC420 Team100 Group Project - Image Inpainting

### Introduction:
In this project, we adapt the pipeline from <a href="https://arxiv.org/abs/1901.00212">EdgeConnect</a>. Our goal is to investigate if adding synthesized gradients will provide more structural guidance, making it easier for the inpainting model to recover image content. Our two-stage pipeline is adapted from the EdgeConnect architecture. In the first stage, gradient and edge generation models recover structural information for masked regions. In the second stage, the synthesized gradients and edges help the inpainting model to fill in the masked RGB image. A more detailed description can be found in our project report.
<p align='center'>  
  <img src='https://user-images.githubusercontent.com/29292822/102656400-d2c90080-4141-11eb-83a0-7c1a801f5493.png' width='870'/>
</p>
<p align='center'>  
  <img src='https://user-images.githubusercontent.com/29292822/102656443-e1171c80-4141-11eb-9ee8-bb2573ab3736.png' width='870'/>
</p>
<p align='center'>  
  <img src='https://user-images.githubusercontent.com/29292822/102656539-07d55300-4142-11eb-881a-812824446935.png' width='870'/>
</p>
Each row above consists of: Input images | Input images with missing regions. The missing regions are depicted in white | Generated edge maps | Generated gradient maps | inpainting model output | synthesized image 

## Prerequisites
- Python 3.6
- PyTorch 1.0
- NVIDIA GPU + CUDA cuDNN

## Models
### 1) Model 3: EdgeConnect
We trained the EdgeConnect pipeline with 128x128 inputs for 2e5 iterations.

### 2) Model 8: Gradient-Edge Connect
Our modified version of EdgeConnect, which takes in generated edges and gradients along with the masked image as input.
<p align='center'>  
  <img src='https://user-images.githubusercontent.com/29292822/102560118-76ada000-409f-11eb-9ac2-177529d7793b.png' width='870'/>
</p>

## Inpainting Demo Tool
run demo.bat to start the tool. [Video of demo](https://drive.google.com/file/d/1lPRV5g5hp_o1I2Bk8E1caa16rPHk7Buh/view?usp=sharing)

A window with instructions will pop up and there's a button to upload an image

After loading an image, use the mouse to draw

Press space = change brush size

Press backspace = reset

Press ESC = exit and save mask

Close the upload window to start inpainting, the inpaint result will be opened and generated in the test_output folder.


## Datasets
### 1) Images
We use [Places2](http://places2.csail.mit.edu) Standard small images dataset, which consists of 1.8 million images of various scene categories.

After downloading, run [`scripts/flist.py`](scripts/flist.py) to generate train, test and validation set file lists. For example, to generate the training set file list on the Places2 dataset, run:
```bash
mkdir datasets
python ./scripts/flist.py --path path_to_places2_train_set --output ./datasets/places_train.flist
```

### 2) Irregular Masks
Our model is trained on the irregular mask dataset from [QD-IMD](https://github.com/karfly/qd-imd) dataset. Before using these masks, first invert the black and white pixels, so the convention is consistent with EdgeConnect.

Please use [`scripts/flist.py`](scripts/flist.py) to generate train, test and validation set masks file lists as explained above.

## Getting Started (instructions adapted from <a href="https://arxiv.org/abs/1901.00212">EdgeConnect</a>)
Download the pre-trained models using the following links and copy them under `./checkpoints` directory. These models are trained with input size 128x128 for 2e5 iterations.
[model 8: GradientEdgeConnect](https://drive.google.com/file/d/1TXluV4CrEWCf0nHTxerhWjJ3HwZKkhxh/view?usp=sharing) | [model 3: modifiedEdgeConnect](https://drive.google.com/file/d/1tjGkCDAWLURAN9d9dJM8Oh7UVqwsJgMm/view?usp=sharing)

### 1) Training
To train the model, create a `config.yaml` file similar to the [example config file](config.yml.example) and copy it under your checkpoints directory. Read the [configuration](#model-configuration) guide for more information on model configuration.

The original EdgeConnect pipeline has 4 training modes and we added the training modes 5 to 9: 
1) model=1: training the edge generation model
2) model=2: training the inpainting model using ground truth edges
3) model=3: training the inpainting model, using edges synthesized by a given edge generation model
4) model=4: training the edge generation and inpainting models at the same time
5) Model=5: training the inpainting model with ground truth edges and ground truth gradients
6) Model=6: training the inpainting model, edge generation model and gradient generation model all at the same time
7) Model=7: training the gradient generation model
8) Model=8: training the inpainting model, using edges synthesized by edge generation model and gradients synthesized by gradient generation model
9) Model=9: training the inpainting model using ground truth gradients

To train the model, call:
```bash
python train.py --model [model_number] --checkpoints [path to checkpoints]
```

For example, to train the two-stage pipeline using synthesized gradients and edges under `./checkpoints/gradientEdgeConnect` directory:
```bash
python train.py --model 8 --checkpoints ./checkpoints/gradientEdgeConnect
```

The number of training iterations can be modified by changing `MAX_ITERS` value in the configuration file.

### 2) Testing
To test the model, create a `config.yaml` file similar to the [example config file](config.yml.example) and copy it under your checkpoints directory. Read the [configuration](#model-configuration) guide for more information on model configuration.

You can test the model for different model numbers (same as training modes 1-9). In each case, you need to provide an input image and a grayscale mask file. Please make sure that the mask file covers the entire mask region in the input image. To test the model:
```bash
python test.py \
  --model [model_number] \
  --checkpoints [path to checkpoints] \
  --input [path to input directory or file] \
  --mask [path to masks directory or mask file] \
  --output [path to the output directory]
```

We provide some test set images under `./examples` directory. Please download the [pre-trained models](#getting-started) and run:
```bash
python test.py \
  --model 8
  --checkpoints ./checkpoints/gradientEdgeConnect
  --input ./examples/test1000resized
  --mask ./examples/mask1000
  --output ./checkpoints/results
```
This script will inpaint all images in `./examples/test1000resized` using their corresponding masks in `./examples/mask1000` directory and saves the results in `./checkpoints/results` directory. By default `test.py` script is run on stage 3 (`--model=3`).

### 3) Evaluating (scripts are from EdgeConnect)
To evaluate the model, you need to first run the model in test mode against your and save the results on disk. Use [`./scripts/metrics.py`](scripts/metrics.py) to evaluate the model using PSNR, SSIM and Mean Absolute Error:

```bash
python ./scripts/metrics.py --data-path [path to validation set] --output-path [path to model output]
```

To measure the Fréchet Inception Distance (FID score) run [`./scripts/fid_score.py`](scripts/fid_score.py). The PyTorch implementation of FID references [this](https://github.com/mseitzer/pytorch-fid) which uses the pre-trained weights from PyTorch's Inception model.

```bash
python ./scripts/fid_score.py --path [path to validation, path to model output] --gpu [GPU id to use]
```

### Model Configuration

The model configuration is stored in a [`config.yaml`](config.yml.example) file under your checkpoints directory. There are 5 new models in comparison to the original EdgeConnect configuration (details are listed in the model training section). The following tables provide the documentation for all the options available in the configuration file:

#### General Model Configurations

Option      	| Description
----------------| -----------
MODE        	| 1: train, 2: test, 3: eval
MODEL       	| 1: edge model, 2: inpaint model with GT edge, 3: edge-inpaint model, 4: joint model, 5: inpaint model with GT edge and GT gradient, 6: edge and gradient joint model, 7: gradient model, 8: edge-gradient-inpaint model, 9: gradient-inpaint model
MASK        	| 1: random block, 2: half, 3: external, 4: external + random block, 5: external + random block + half
EDGE        	| 1: canny, 2: external
NMS         	| 0: no non-max-suppression, 1: non-max-suppression on the external edges
SEED        	| random number generator seed
GPU         	| list of gpu ids, comma separated list e.g. [0,1]
DEBUG       	| 0: no debug, 1: debugging mode
VERBOSE     	| 0: no verbose, 1: output detailed statistics in the output console

#### Loading Train, Test and Validation Sets Configurations

Option      	| Description
----------------| -----------
TRAIN_FLIST 	| text file containing training set files list
VAL_FLIST   	| text file containing validation set files list
TEST_FLIST  	| text file containing test set files list
TRAIN_EDGE_FLIST| text file containing training set external edges files list (only with EDGE=2)
VAL_EDGE_FLIST  | text file containing validation set external edges files list (only with EDGE=2)
TEST_EDGE_FLIST | text file containing test set external edges files list (only with EDGE=2)
TRAIN_MASK_FLIST| text file containing training set masks files list (only with MASK=3, 4, 5)
VAL_MASK_FLIST  | text file containing validation set masks files list (only with MASK=3, 4, 5)
TEST_MASK_FLIST | text file containing test set masks files list (only with MASK=3, 4, 5)

#### Training Mode Configurations

Option             	|Default| Description
-----------------------|-------|------------
LR                 	| 0.0001| learning rate
D2G_LR             	| 0.1   | discriminator/generator learning rate ratio
BETA1              	| 0.0   | adam optimizer beta1
BETA2              	| 0.9   | adam optimizer beta2
BATCH_SIZE         	| 8 	| input batch size
INPUT_SIZE         	| 128   | input image size for training. (0 for original size)
SIGMA              	| 2 	| standard deviation of the Gaussian filter used in Canny edge detector </br>(0: random, -1: no edge)
MAX_ITERS          	| 2e5   | maximum number of iterations to train the model
EDGE_THRESHOLD     	| 0.5   | edge detection threshold (0-1)
L1_LOSS_WEIGHT     	| 1 	| l1 loss weight
FM_LOSS_WEIGHT     	| 10	| feature-matching loss weight
STYLE_LOSS_WEIGHT  	| 1 	| style loss weight
CONTENT_LOSS_WEIGHT	| 1 	| perceptual loss weight
INPAINT_ADV_LOSS_WEIGHT| 0.01  | adversarial loss weight
GAN_LOSS           	| nsgan | **nsgan**: non-saturating gan, **lsgan**: least squares GAN, **hinge**: hinge loss GAN
GAN_POOL_SIZE      	| 0 	| fake images pool size
SAVE_INTERVAL      	| 1000  | how many iterations to wait before saving model (0: never)
EVAL_INTERVAL      	| 0 	| how many iterations to wait before evaluating the model (0: never)
LOG_INTERVAL       	| 10	| how many iterations to wait before logging training loss (0: never)
SAMPLE_INTERVAL    	| 1000  | how many iterations to wait before saving sample (0: never)
SAMPLE_SIZE        	| 12	| number of images to sample on each sampling interval

## Citation
This project is built based on EdgeConnect.
<a href="https://arxiv.org/abs/1901.00212">EdgeConnect: Generative Image Inpainting with Adversarial Edge Learning</a>

<a href="http://openaccess.thecvf.com/content_ICCVW_2019/html/AIM/Nazeri_EdgeConnect_Structure_Guided_Image_Inpainting_using_Edge_Prediction_ICCVW_2019_paper.html">EdgeConnect: Structure Guided Image Inpainting using Edge Prediction</a>:

```
@inproceedings{nazeri2019edgeconnect,
  title={EdgeConnect: Generative Image Inpainting with Adversarial Edge Learning},
  author={Nazeri, Kamyar and Ng, Eric and Joseph, Tony and Qureshi, Faisal and Ebrahimi, Mehran},
  journal={arXiv preprint},
  year={2019},
}

@InProceedings{Nazeri_2019_ICCV,
  title = {EdgeConnect: Structure Guided Image Inpainting using Edge Prediction},
  author = {Nazeri, Kamyar and Ng, Eric and Joseph, Tony and Qureshi, Faisal and Ebrahimi, Mehran},
  booktitle = {The IEEE International Conference on Computer Vision (ICCV) Workshops},
  month = {Oct},
  year = {2019}
}
```


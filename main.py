import argparse
import torch.nn as nn
import torch
from model import build_model
from train import train
from test import test
from constitution_classifier import classify_constitution

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def get_args():
    parser = argparse.ArgumentParser(description="Train the UNet",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--lr", default=1e-4, type=float, dest="lr")
    parser.add_argument("--batch_size", default=2, type=int, dest="batch_size")
    parser.add_argument("--num_epoch", default=100, type=int, dest="num_epoch")

    parser.add_argument("--transform", default="off", type=str, dest="transform")
    parser.add_argument("--image_size", default=256, type=int, dest="image_size")

    parser.add_argument("--data_dir", default="./dataset/v2", type=str, dest="data_dir")
    parser.add_argument("--result_dir", default="./result", type=str, dest="result_dir")
    parser.add_argument("--log_dir", default="./log", type=str, dest="log_dir")
    parser.add_argument("--ckpt_dir", default="./checkpoint/test", type=str, dest="ckpt_dir")
    parser.add_argument("--num_workers", default=4, type=int, dest="num_workers")

    parser.add_argument("--mode", default="test", type=str, dest="mode")
    parser.add_argument("--model", default="efficientnet", type=str, dest="model")
    parser.add_argument("--train_continue", default="off", type=str, dest="train_continue")
    parser.add_argument("--pretrained", default="off", type=str, dest="pretrained")


    args = parser.parse_args()

    return args

def main(args):
    # Get model by arugment 
    model, optimizer = build_model(args.model, args.lr)

    if args.mode == 'train':  
        train(args, model, optimizer, device)

    else: 
        test(args, model, optimizer, device)
        
        # Classify constitution based on predicted mask.
        classify_constitution()
        

if __name__ == '__main__':
    args = get_args()
    main(args)


#!/usr/bin/python3

from PIL import Image
import numpy as np
import os, sys, argparse


def main():
    parser = argparse.ArgumentParser(description='Convert 16B tiff to 8B tiff.')
    parser.add_argument(dest="filenames", metavar="F", type=str, nargs='+', help="16B tiff filename to convert")
    args = parser.parse_args()
    for filename in args.filenames:
        if os.path.exists("./{}".format(filename)):
            convert(filename) 
        else:
            print("Couldn't find {}".format(filename))


def convert(filename):
    im = Image.open(filename)
    print("reading {}, Format:{}, Size:{}, Mode:{}, Frame Number:{}".format(filename, im.format, im.size, im.mode, im.n_frames))
    for i in range(im.n_frames):
        im.seek(i)
        ar = np.array(im)
        ar = ar / 16

        max_pix = ar.max()
        min_pix = ar.min()
        pix_range = max_pix - min_pix  
        out_range = 256
        ar = (ar - min_pix)/pix_range*out_range

        pilImg = Image.fromarray(np.uint8(ar))
        out_filename = "out_{}_{}.tiff".format(filename.split(".")[0], i) 
        pilImg.save(out_filename)
        print("Converted {} frame No.{} to {}".format(filename, i+1, out_filename))


if __name__ == "__main__":
    main()
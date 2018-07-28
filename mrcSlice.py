#!/home/gao/.pyenv/shims/python

from PIL import Image
import numpy as np
import os, sys, argparse, mrcfile

def main():
    parser = argparse.ArgumentParser(description='output averaged mrc slice as png')
    parser.add_argument(dest="mrcfilename", type=str, nargs=1, help="name of mrcfile to convert")
    parser.add_argument('-n', '--num', dest="stacknum", type=int, nargs='?', default=30, help="number of mrc slices to average in one stack, default is 30")
    parser.add_argument('--sapce', '-s', dest="space", type=int, nargs='?', default=30, help="number of mrc slices between each outputs, default is 30")
    parser.add_argument('--axis', '-a', dest="axis", type=str, nargs='?', choices=['x', 'X', 'y', 'Y', 'z', 'Z'], default='y', help="stack or slice direction")
    args = parser.parse_args()
    mrcfilename = args.mrcfilename[0]
    mrc = mrcfile.mmap(mrcfilename)
    axis = args.axis[0]
    if axis in {'x', 'X'}:
        vol = mrc.data.transpose(2,0,1)
    elif axis in {'y', 'Y'}:
        vol = mrc.data.transpose(1,2,0)
    else:
        #slice along z-axis, needless to transpose vol
        vol = mrc.data
    mrc.close
    z, y, x = vol.shape
    stacknum = args.stacknum
    space = args.space
    if z < stacknum:
        print("ERR: inputed stacknumber({}) exceeded total slices along {}-axis.".format(stacknum, axis)) 
        sys.exit()
    print("Start processing {}.".format(mrcfilename))
    for stack_begin in range(0, z - stacknum, space):
        z_stack = np.sum(vol[stack_begin:stack_begin+stacknum, :, :], axis=0)
        pix_max = z_stack.max()
        pix_min = z_stack.min()
        pix_range = pix_max - pix_min
        out_range = 256
        im = np.uint8((z_stack - pix_min) / pix_range * out_range)
        out_name = "out_{}_{}_{}.png".format(mrcfilename, stack_begin, stack_begin+stacknum-1)
        Image.fromarray(im).save(out_name)
        print("Generated {}.".format(out_name))
    print("Finished processing {}.".format(mrcfilename))


if __name__=='__main__':
    main()
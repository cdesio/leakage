#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import os, re, sys

def extract_pixels(data_folder, fnames, prefix, tint, a, b, label_list, pix_shift):
    regex = re.compile(r'\d+')
    rad_dam = label_list

    shift = pix_shift
    avg_pixels = np.zeros((len(fnames), len(rad_dam)))

    pixels = np.zeros((len(fnames), len(rad_dam)), dtype=object)
    for i, f in enumerate(fnames):
        print(f)
        fpath = os.path.join(data_folder, prefix, tint, f)
        im_read = plt.imread(fpath)
        iter_rad_dam = iter(rad_dam)
        j=0
        for xa in a:
            for xb in b:
                label=next(iter_rad_dam)
                sel = im_read[xb-shift:xb+shift, xa-shift:xa+shift]
                pixels[i, j]=sel
                for p in sel:
                    if np.any(p<20):
                        bad = np.where(p<20)[0]
                        p[bad] = int(np.ceil(np.mean([p[bad-1], p[bad+1]])))
                    avg_pixels[i, j]=np.ceil(np.mean(sel))
                j+=1
        plt.close()

    fout = os.path.join(data_folder,'extracted', '_'.join([prefix, tint,'sh'+str(pix_shift)+'.npz']))
    print('saving to {}'.format(fout))
    np.savez_compressed(fout, pixels = pixels, avg=avg_pixels)
    return

def coordinate_list(keyword):
    if keyword=='rad_dam':
        a0=580
        a1=440
        a_shift = 402

        a = [a0+alpha*a1+beta*a_shift for alpha, beta in zip([0,1,1,1],[0,0,1,2])]

        b0=360
        b1=420
        b_shift = 402

        b = [b0+alpha*b1+beta*b_shift for alpha, beta in zip([0,1,1,1,1],[0,0,1,2,3])]
        label_list = [50, 45, 40, 35, 30, 20, 18, 16, 14, 12, 10, 9, 8, 25, 6, 5, 4, 3, 2, 1]

    elif keyword=='no_dam':
        a0=200
        a1=1000
        a_shift = 750
        a = [a0+ alpha*a1 + beta * a_shift for alpha,beta in zip([0,1,1], [0,0,1])]

        b0=120
        b1=1000
        b_shift = 1150
        b = [b0+alpha*b1+beta*b_shift for alpha,beta in zip([0,1,1], [0,0,1])]
        label_list = [1, 2, 3, 4, 5, 6, 7, 8,9]
    return a, b, label_list




if __name__=='__main__':
    regex = re.compile(r'\d+')
    print('run')
    data_folder = sys.argv[1]
    keyword = sys.argv[2]
    print(data_folder)
    a, b, label_list = coordinate_list(keyword)
    
    for root, dirs, files in os.walk(data_folder):

        if len(dirs)>0:
            #print(os.path.split(root)[1], dirs)
            for tint in dirs:
                prefix = os.path.split(root)[1]
                if prefix.startswith('T'):
                    print(prefix,tint)
                    if tint.startswith('Tint'):
                        fnames = os.listdir(os.path.join(data_folder,prefix,tint))
                        n_files = []
                        for f in fnames:
                            n_files.append(int(regex.findall(f)[0]))
                        sorted_fnames = np.array(fnames)[np.argsort(n_files)]
                        extract_pixels(data_folder, sorted_fnames, prefix, tint, a, b, label_list, pix_shift=10)

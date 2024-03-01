import os
import numpy as np
from PIL import Image as Image
from argparse import ArgumentParser

def centre_crop(image, mask, ratio = 1.5):
    ii,jj = np.where(mask>0)

    width = max(jj)-min(jj)
    height = max(ii)-min(ii)

    tl = [min(ii), min(jj)]
    br = [max(ii), max(jj)]
    tr = [tl[0], br[1]]
    bl = [br[0], tl[1]] 
    
    b_width = width*ratio
    b_height = height*ratio

    delta_w = int((b_width-width)*0.5)
    delta_h = int((b_height-height)*0.5)

    h,w = mask.shape
    b_tl = [max(0,tl[0]-delta_h), max(0,tl[1]-delta_w)]
    b_br = [min(h,br[0]+delta_h), min(w,br[1]+delta_w)]
    b_tr = [b_tl[0], b_br[1]]
    b_bl = [b_br[0], b_tl[1]] 

    cropped_image = image[b_tl[0]:b_bl[0],b_tl[1]:b_tr[1]]
    cropped_mask = mask[b_tl[0]:b_bl[0],b_tl[1]:b_tr[1]]
    
    return cropped_image, cropped_mask 


def crop_all(im_dir, mask_dir, im_outdir, mask_outdir, im_ext, mask_ext):
    os.makedirs(im_outdir)
    os.makedirs(mask_outdir)
    for im in os.listdir(im_dir):
        image = np.array(Image.open(os.path.join(im_dir,im)))
        mask_name = im.replace(im_ext,mask_ext)
        if os.path.exists(os.path.join(mask_dir,mask_name)):
            mask = np.array(Image.open(os.path.join(mask_dir,mask_name)))
            if len(mask.shape)>2:
                mask = mask[:,:,0]
            if mask.sum().sum()>0:
                image_c, mask_c = centre_crop(image, mask, ratio = 1.5) 
                Image.fromarray(image_c).save(os.path.join(im_outdir,im))
                Image.fromarray(mask_c).save(os.path.join(mask_outdir,im.replace(im_ext,mask_ext)))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--data_dir', default='../dataset/', required=True)
    parser.add_argument('--type', default='still', required=True)
    parser.add_argument('--im_ext', default='.jpg') 
    parser.add_argument('--mask_ext', default='.png')  
    parser.add_argument('--out_data_dir', default='../dataset_crop/') 

    args = parser.parse_args()

    if args.type == 'still':    
        f_args = {'im_dir': os.path.join(args.data_dir,'Imgs'),
            'mask_dir': os.path.join(args.data_dir,'GT'),
            'im_outdir': os.path.join(args.out_data_dir,'Imgs'),
            'mask_outdir': os.path.join(args.out_data_dir,'GT'),
            'im_ext':args.im_ext,
            'mask_ext' : args.mask_ext}
        crop_all(**f_args)
        
    else:

        vid_list = os.listdir(args.data_dir)        
        for v in vid_list:
            v_args = {'im_dir':os.path.join(args.data_dir,v,'Imgs'),
            'mask_dir':os.path.join(args.data_dir,v,'GT'),
            'im_outdir':os.path.join(args.out_data_dir,v,'Imgs'),
            'mask_outdir':os.path.join(args.out_data_dir,v,'GT'),
            'im_ext':args.im_ext,
            'mask_ext' : args.mask_ext}

            crop_all(**v_args)

import os
from argparse import ArgumentParser
from scores.perceptual_scores import compute_Srf, compute_Sb, compute_S_alpha 
import pandas as pd
import numpy as np
from PIL import Image as Image
from scores.perceptual_scores import compute_S_alpha
from utils.trimap import erode_dilate_fg

def compute_scores(im_dir,mask_dir,contour_path,contour_gt_path,im_ext,mask_ext,alpha,out_dir):
    col_names = ['imname', 'S_rf', 'S_b', 'S_alpha']
    if not os.path.exists(args.out_dir):
          os.makedirs(args.out_dir)
    f_name = args.out_dir+'/scores.csv'
    df = pd.DataFrame(columns=col_names)
    with open(f_name, 'w') as f:
        df.to_csv(f, header=False,index=False)

    list_dir = os.listdir(im_dir)
    list_dir.sort() 
    for name in list_dir:
            img_name = name
            mask_name = img_name.replace(im_ext,mask_ext)
            
            fg_mask = np.array(Image.open(os.path.join(mask_dir,mask_name)))/255
            img =  np.array(Image.open(os.path.join(im_dir,name)))/255
            trimap = erode_dilate_fg(fg_mask) 

            im_c = np.array(Image.open(os.path.join(contour_path,mask_name)))/255
            im_c_gt = np.array(Image.open(os.path.join(contour_gt_path,mask_name)))/255

            try:  
                    Srf, Sb, S_alpha = compute_S_alpha(alpha,img,trimap, im_c, im_c_gt, out_dir,img_name[:-4],return_all=True)
            except:
                    score = -1 
                    inner = -1
            df_im = pd.DataFrame(columns=col_names).append({'imname':name,'S_rf':Srf, 'S_b':Sb, 'S_alpha': S_alpha},ignore_index=True)
            df_im.to_csv(f_name, mode='a', header=False, index=False)





if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--data_dir', default='../dataset/', required=True)
    parser.add_argument('--type', default='still', required=True)
    parser.add_argument('--contour_path', default='../dataset/contours/', required=True)
    parser.add_argument('--contour_gt_path', default='../dataset/contours_gt/', required=True)
    parser.add_argument('--im_ext', default='.jpg') 
    parser.add_argument('--mask_ext', default='.png') 

    parser.add_argument('--out_dir', default='out_dir/') 
    parser.add_argument('--score', default='Combined', choices=['Srf','Sb','Combined'])
    parser.add_argument('--alpha', default=0.35)
    
    args = parser.parse_args()
    if args.type=='still':
            f_args = {'im_dir': os.path.join(args.data_dir,'Imgs'),
            'mask_dir': os.path.join(args.data_dir,'GT'),
            'contour_path': args.contour_path,
            'contour_gt_path': args.contour_gt_path,
            'im_ext': args.im_ext,
            'mask_ext' : args.mask_ext,
            'alpha': args.alpha,
            'out_dir': args.out_dir}

            compute_scores(**f_args)
    else:
        
        vid_list = os.listdir(args.data_dir)        
        for v in vid_list:
            v_args = {'im_dir':os.path.join(args.data_dir,v,'Imgs'),
            'mask_dir':os.path.join(args.data_dir,v,'GT'),
            'contour_path': os.path.join(args.contour_path,v),
            'contour_gt_path': os.path.join(args.contour_gt_path,v),
            'im_ext': args.im_ext,
            'mask_ext' : args.mask_ext,
            'alpha': args.alpha,
            'out_dir': os.path.join(args.out_dir,v)}

            compute_scores(**v_args)
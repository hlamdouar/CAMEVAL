from PIL import Image as Image
import numpy as np
from sklearn.metrics import f1_score
import os
from utils.ann import ann



#Reconstruction Fidelity Score
def compute_Srf(img,trimap, out_dir,im_name,w=7,save_output=True):
    #trimap
    mask_erode,mask_dilate = trimap
    im_masked_fg = (mask_erode.reshape(mask_erode.shape[0],mask_erode.shape[1],1)*img)
    im_masked_bg = ((1-mask_dilate.reshape(mask_dilate.shape[0],mask_dilate.shape[1],1))*img)

    if not os.path.exists(out_dir+'/temp/'):
        os.makedirs(out_dir+'/temp/')
        
    Image.fromarray((im_masked_fg*255).astype(np.uint8)).save(out_dir+'/temp/'+im_name+'.jpg')
    Image.fromarray((im_masked_bg*255).astype(np.uint8)).save(out_dir+'/temp/'+im_name+'inv.jpg')


    #compute fg features
    ns = im_masked_fg.shape
    idx_fg = []
    fg_feat_v=[]
    d = int(w/2)
    for x in range(0,ns[0]-w,d):
        for y in range(0,ns[1]-w,d):
            if (mask_erode[x:x+w,y:y+w]>0).all():
                idx_fg.append([x,y])
                fg_feat_v.append(np.array(im_masked_fg[x:x+w,y:y+w,:]).reshape(-1,w*w*3).astype(np.float32))
    fg_feat_v_ = np.concatenate(fg_feat_v,axis=0)
    
    #compute bg features
    mask_inv = 1.-mask_dilate
    idx_bg = []
    bg_feat_v=[]
    for x in range(0,ns[0]-w,d):
        for y in range(0,ns[1]-w,d):
            if (mask_inv[x:x+w,y:y+w]>0).all():
                idx_bg.append([x,y])
                bg_feat_v.append(np.array(im_masked_bg[x:x+w,y:y+w,:]).reshape(-1,w*w*3).astype(np.float32))
    bg_feat_v_ = np.concatenate(bg_feat_v,axis=0)

    #get fg's bg nearest neighbour
    fg_nn = ann(bg_feat_v_, fg_feat_v_, dims=w*w*3, m=3) 


    img_recon = np.zeros((ns[0], ns[1],3))

    counts = np.zeros((ns[0], ns[1]))+0.000001
    for i in range(len(idx_fg)):
        x,y = idx_fg[i]
        nn_i_j =  fg_nn[i][0]
        cii, cjj = idx_bg[nn_i_j]
        img_recon[x:x+w,y:y+w,:] +=im_masked_bg[cii:cii+w,cjj:cjj+w,:]
        counts[x:x+w,y:y+w] += 1 

    counts=np.reshape(counts,(ns[0], ns[1],1))
    img_recon = img_recon/counts

    #compute score
    mask= np.abs(im_masked_fg-img_recon).sum(2)<0.2*im_masked_fg.sum(2)
    mask.resize(ns[0],ns[1],1)
    score = mask.sum()/mask_erode.sum()
    out_im =img_recon+im_masked_bg

    if save_output:
        Image.fromarray(((out_im)*255).astype(np.uint8)).save(out_dir+'/'+im_name+'reconstructed.jpg')   

    return score

#Boundary Score
def compute_Sb(im_c, im_c_gt,trimap):
    mask_erode,mask_dilate = trimap
    im_c = im_c<0.5
    im_c_gt = im_c_gt<0.5
    
    mask = mask_erode+1-mask_dilate
    true_ = []
    predict = []
    for i in np.arange(mask.shape[0]):
        for j in np.arange(mask.shape[1]):
            if mask[i,j]==0:
                true_.append(im_c_gt[i,j])
                predict.append(im_c[i,j])
    F1 = f1_score(np.array(true_).astype(int), (np.array(predict)).astype(int), average='macro')
    
    return 1-F1

#Combined score
def compute_S_alpha(alpha,img,trimap, im_c, im_c_gt, out_dir,im_name,w=7,save_output=True,return_all=True):
   Srf = compute_Srf(img,trimap, out_dir,im_name,w=w,save_output=save_output)
   Sb = compute_Sb(im_c, im_c_gt,trimap)
   if return_all:
       return Srf, Sb, (1-alpha)*Srf+alpha*Sb 
   return (1-alpha)*Srf+alpha*Sb

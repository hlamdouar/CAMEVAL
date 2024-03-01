import numpy as np
import cv2

def erode_dilate_fg(fg_mask, it=3 , r_min=0.7, r_max=0.8):
    assert r_min<r_max, "r_min should be less or equal to r_max"
    kernel_sz = np.arange(1,21,2)
    i=0
    sz_found=False
    while i< len(kernel_sz) and not sz_found:
        k = kernel_sz[i] 
        kernel = np.ones((k,k),np.uint8)
        mask_erode = cv2.erode(fg_mask,kernel,iterations = it)
        ratio = mask_erode.sum()/fg_mask.sum()
        
        if ratio<r_max and ratio>=r_min:
            sz_found = True
            mask_dilate = cv2.dilate(fg_mask,kernel,iterations = it)
        i = i+1
    
    if not sz_found:
        k = 3
        kernel = np.ones((k,k),np.uint8)
        mask_erode = cv2.erode(fg_mask,kernel,iterations = it)
        mask_dilate = cv2.dilate(fg_mask,kernel,iterations = it)
    return mask_erode, mask_dilate 
# The Making and Breaking of Camouflage

<img src="asset/examples.png" width="800">

### Dataset Preparation Steps
<ol>
<li>Crop the images around the camouflaged animal so that only its immediate surrounding area is taken into account: 

Examples:

For a still image dataset:
```
python utils/crop.py --data_dir ../datasets/CHAMELEON --out_data_dir ../datasets/CHAMELEON_crop --type still
```

For a video dataset:
```
python utils/crop.py --data_dir ../datasets/MoCA_Video/TrainDataset_per_sq/ --out_data_dir ../datasets/Moca_Video_Train_crop --type video
```
</li> 
<li> To compute the boundary score and the combined score, generate global contours (for the cropped images) and ground truth contours (for the object of interest, using the mask) with an off-the-shelf contour detection method, e.g. [DexiNed](https://github.com/xavysp/DexiNed)</li> 
</ol>

### Citation

If you find this repo useful for your research, please consider citing our paper: 

```
@InProceedings{Lamdouar23,
  author       = "Hala Lamdouar and Weidi Xie and Andrew Zisserman",
  title        = "The Making and Breaking of Camouflage",
  booktitle    = "IEEE International Conference on Computer Vision",
  year         = "2023",
}
```
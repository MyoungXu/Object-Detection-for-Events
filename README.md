# Object-Detection-for-Events
这个工程记录我自己跑通的一些代码，并介绍怎么在自己电脑上运行。


原YOLOv5代码可以在[这里](https://github.com/ultralytics/yolov5)找到

DSEC数据集目标检测标签可以在[这里](https://dsec.ifi.uzh.ch/dsec-detection/)找到
  
## 环境

* 建议使用python3.8
```
conda create --name HRNet python=3.8.18
```
* 我自己用的torch版本
```bash
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch
```
* 其他需要的库
```bash
pip install -r requirements.txt
```


## 运行前的准备
在工程的`./dataset_to_be_detected/all_DSEC_labels`里面，我已经把所有的目标检测标签按照名字放好了，可是运行程序还需要有时间戳和重建图。
* 时间戳可以在DSEC官网的[这里](https://dsec.ifi.uzh.ch/dsec-datasets/download/)找到，把需要的数据集的`timestamps.txt`放在`track.npy`同一个文件夹即可。比如都放在`./dataset_to_be_detected/all_DSEC_labels/zurich_city_09_a`中即可。
* 重建图不用直接放进文件夹，在后续操作的`xjh.py`里会处理的。但是需要注意的是，理论上重建图像需要和时间戳对应（数量）。如果数量不一致，请修改`xjh.py`。如果重建图像相比时间戳只少了第一张和最后一张，也可以直接运行`xjh2.py`。

## 运行
一、运行`xjh.py	`
```bash
python xjh.py --nt PATH-TO-TIMESTAMP-FOLDER --p PATH-TO-PICTURES
```
其中`PATH-TO-TIMESTAMP-FOLDER`应该修改为存放timestamps.txt和tracks.npy的文件夹地址。`PATH-TO-PICTURES`应该修改为需要检测的图像所在的文件夹地址。

**示例**：
```bash
python xjh.py --nt dataset_to_be_detected/all_DSEC_labels/zurich_city_09_a --p /mnt/data/xujinghan//dsec/zurich_city_09_a
```

二、运行`val.py`
```bash
python val.py --save-txt --save-conf --name FOLDER-NAME
```
其中`FOLDER-NAME`需要修改为自己指定的名字。
后续运行结果可以在`./runs/val/FOLDER-NAME`里面找到

**示例**：
```bash
python val.py --save-txt --save-conf --name 09_a
```

三、运行`draw.py`

```bash
python draw.py --p PATH-TO-LABEL-FOLDER
```
其中`PATH-TO-LABEL-FOLDER`应该修改为上面`val.py`结果保存的路径。
随后，可以在`./runs/val/FOLDER-NAME/box`里找到带框的检测结果。

**示例**：
```bash
python draw.py --p runs/val/09_a
```

四、（可选）运行`draw_origin.py`
```bash
python draw_origin.py --s SAVE-PATH
```
这个代码的作用为：将真实标签画在图上，可用作对比观察。其中`SAVE-PATH`可以改为自己想要的地方。如果没有输入，则默认保存在`./dataset_to_be_detected/images/origin`里。

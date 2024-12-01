# Hasil Training
Adjustment for all:
[yolo] and [convolutional] before [yolo] layer

    --> number of classes = 2 
    --> filters = (2 + 5)*3 (only in each layer before [yolo] layer), 

All training here uses crowdhuman data
NOTE: Jam pada g colab adalah jam server (UTC, bukan UTC + 7 yang dipakai di Indo)

# YOLOv4 - Training_0_[31-01-2021]

Trained on: HP Pavilion 15 dk1064tx
yolov4 normal on yolov4.conv.137 (yolov4 pretrained weights) 

![](https://cdn.discordapp.com/attachments/806343914058809354/806344000431980544/unknown.png)

![](https://cdn.discordapp.com/attachments/806343914058809354/806344073265807390/chart.png)

# YOLOv4 - Training_1_[23-03-2021 - 29-03-2021] 

Trained on: HP Pavilion 15 dk1064tx
config file:

https://www.dropbox.com/s/5vpar9rjds92mfs/yolov4-custom-crowdhuman-1.cfg?dl=0


yolov4 normal from zero configs:
 - training is from ZERO (not using yolov4.conv.137) 
 - yolov4 archi adjusted in 

    → input width and height size = 416 * 416
    --> batch = 64, 
    --> subdivisions = 64, 
    --> steps = 4800, 5400, 
    --> max batch size = 6000, 
    --> width = 416 and height = 416

augmentation used:
mosaic=1
mixup=1
blur=1
flip=1
current result

![](https://cdn.discordapp.com/attachments/806343914058809354/823610969157795850/unknown.png)

![](https://cdn.discordapp.com/attachments/806343914058809354/823618542733754368/unknown.png)

![](https://cdn.discordapp.com/attachments/806343914058809354/823718843281178624/unknown.png)

![](https://cdn.discordapp.com/attachments/806343914058809354/823942478008156170/chart_yolov4-custom-crowdhuman-1.png)

![](https://cdn.discordapp.com/attachments/806343914058809354/825785052108423188/unknown.png)

![](https://cdn.discordapp.com/attachments/806343914058809354/825788423851737148/unknown.png)


training continued from batch 6001 to 12000 

- using these configs max_batches = 12000 
- policy=steps 
- steps=4800,5400 
- scales=.1,.1
![](https://cdn.discordapp.com/attachments/806343914058809354/826225048057544734/unknown.png)

![](https://cdn.discordapp.com/attachments/806343914058809354/826331713684111390/unknown.png)

![](https://cdn.discordapp.com/attachments/806343914058809354/826465227872403476/8d41ccad-1c32-4537-bc4a-341070094173.png)

![](https://cdn.discordapp.com/attachments/806343914058809354/826465285367398410/b376c57f-b751-4cdf-a01e-492fe7b23f35.png)

# YOLOv4 - Training_2_[17-04-2021 - 19-04-2021]

Trained on: HP Pavilion 15 dk1064tx
yolov4 normal from zero configs:

https://www.dropbox.com/s/rylteltlqg3rha9/yolov4-custom-crowdhuman-2.cfg?dl=0


 - training is from ZERO (not using yolov4.conv.137) 
 - yolov4 archi adjusted in 

    --> batch = 64, 
    --> subdivisions = 64, 
    → input width and height size = 512 * 512
    --> steps = 4800, 5400, 
    --> max batch size = 6000, 
    --> width = 416 and height = 416

augmentation used:
mosaic=1
mixup=1
blur=1
flip=1
current result

![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619113933005_chart_yolov4-custom-crowdhuman-2_1.png)

![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619113932983_chart_yolov4-custom-crowdhuman-2_2.png)

# YOLOv4 - Training_3_[17-04-2021 - 19-04-2021]

Trained on: HP Pavilion 15 dk1064tx
yolov4 normal from zero configs:

https://www.dropbox.com/s/19n41nbdbmb3ixn/yolov4-custom-crowdhuman-3.cfg?dl=0


 - training is from ZERO (not using yolov4.conv.137) 
 - yolov4 archi adjusted in 

    --> batch = 64, 
    --> subdivisions = 64, 
    → input width and height size = 512 * 512
    --> steps = 4800, 5400, 
    --> max batch size = 6000, 
    --> width = 320 and height = 320

augmentation used:
mosaic=1
mixup=1
blur=1
flip=1
current result

![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619353675851_s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619114140415_chart_yolov4-custom-crowdhuman-3.png)

# YOLOv4 - Training_4_[25-04-2021]

Trained on: HP Pavilion 15 dk1064tx
yolov4 normal using transfer learning configs:

https://www.dropbox.com/s/s6obvnpwbcve3gq/yolov4-custom-crowdhuman-tf-1.cfg?dl=0


- transfer learning (using yolov4.conv.137) 
 - yolov4 archi adjusted in 

    --> batch = 64, 
    --> subdivisions = 36, 
    → input width and height size = 416 * 416
    --> steps = 4800, 5400, 
    --> max batch size = 12000
    
![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619364668039_chart_yolov4-custom-crowdhuman-tf-1.png)

# YOLOv4 - Training_5_[25-04-2021]
https://www.dropbox.com/s/qj486cxsyiib32p/yolov4-custom-crowdhuman-tf-2.cfg?dl=0


Trained on GColab

![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619353498572_image.png)

![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619355405508_image.png)

![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619441704498_image.png)

![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619441727447_image.png)


- transfer learning (not using yolov4.conv.137) 
 - yolov4 archi adjusted in 

    --> batch = 64, 
    --> subdivisions = 36, 
    → input width and height size = 416 * 416
    --> steps = 9600, 10800
    --> max batch size = 12000

Current result (25/04/2021 - 19.00)  :

![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619353784167_chart_yolov4-custom-crowdhuman-tf-2+20.png)

# YOLOv4 - Training_6_[25-04-2021]

Trained on: HP Pavilion 15 dk1064tx

https://www.dropbox.com/s/wgobpa8pk8wd978/yolov4-custom-crowdhuman-tf-3.cfg?dl=0


- transfer learning (using yolov4.conv.137) 
 - yolov4 archi adjusted in 

    --> batch = 64, 
    --> subdivisions = 36, 
    → input width and height size = 320 * 320
    --> steps = 4800, 5400, 
    --> max batch size = 12000

result:

![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619442060622_chart_yolov4-custom-crowdhuman-tf-3.png)

# YOLOv4 - Training_7_[25-04-2021]

Trained on: HP Pavilion 15 dk1064tx

https://www.dropbox.com/s/diqmzyws7ysziw3/yolov4-custom-crowdhuman-tf-5.cfg?dl=0


- transfer learning (using yolov4.conv.137) 
 - yolov4 archi adjusted in 

    --> batch = 64, 
    --> subdivisions = 36, 
    → input width and height size = 512 * 512
    --> steps = 4800, 5400, 
    --> max batch size = 12000

OTW

# YOLOv4 - Training_8_[25-04-2021]

Trained on: Google Colab

https://www.dropbox.com/s/k85n2tx3x6nh0b4/yolov4-custom-crowdhuman-tf-4.cfg?dl=0


- transfer learning (using yolov4.conv.137) 
 - yolov4 archi adjusted in 

    --> batch = 64, 
    --> subdivisions = 36, 
    → input width and height size = 320 * 320
    --> steps = 9600, 10800, 
    --> max batch size = 12000

OTW

# YOLOv4_tiny - Training_1_[30_03_2021] 

Trained on: HP Pavilion 15 dk1064tx
yolov4 tiny from zero configs: 

https://www.dropbox.com/s/3i7czwnwr5hvo3f/yolov4-tiny-custom-crowdhuman-1.cfg?dl=0


- training is from ZERO (not using yolov4-tiny.conv.29) 
- yolov4 archi adjusted in 


    --> batch = 64, 
    --> subdivisions = 32, 
    --> max batch size = 17400, 
    --> width = 416 and height = 416 

preprocessing used: 
augmentation used:
mosaic=1
mixup=1
blur=1
flip=1

![](https://cdn.discordapp.com/attachments/806343914058809354/826692981426880522/chart_yolov4-tiny-custom-crowdhuman-1.png)

![](https://cdn.discordapp.com/attachments/806343914058809354/826693873253351454/unknown.png)

# YOLOv4_tiny - Training_2_[30_03_2021]

Trained on: HP Pavilion 15 dk1064tx

https://www.dropbox.com/s/r8r2kjiv6nqhq4y/yolov4-tiny-custom-crowdhuman-2.cfg?dl=0


- training is from ZERO (not using yolov4-tiny.conv.29) 
- yolov4 archi adjusted in 


    --> batch = 64, 
    --> subdivisions = 32,
    --> max batch size = 24000 
    --> width = 416 and height = 416 

preprocessing used: 
augmentation used:
mosaic=1
mixup=1
blur=1
flip=1

![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619188267671_chart_yolov4-tiny-custom-crowdhuman-2.png)

# YOLOv4_tiny - Training_3_[23_03_2021]
https://www.dropbox.com/s/pvwihog83vwgn49/yolov4-tiny-custom-crowdhuman-3.cfg?dl=0


- training is from ZERO (not using yolov4-tiny.conv.29) 
- yolov4 archi adjusted in 

    --> batch = 64, 
    --> subdivisions = 32,

     → steps= 19200, 21600

    --> max batch size = 24000 
    --> width = 320 and height = 320

preprocessing used: 
augmentation used:
mosaic=1
mixup=1
blur=1
flip=1

# YOLOv4_tiny - Training_4_[28_04_2021]
https://www.dropbox.com/s/pvwihog83vwgn49/yolov4-tiny-custom-crowdhuman-3.cfg?dl=0


- training is from ZERO (not using yolov4-tiny.conv.29) 
- yolov4 archi adjusted in 

    --> batch = 64, 
    --> subdivisions = 32,

     → steps= 19200, 21600

    --> max batch size = 24000 
    --> width = 512 and height = 512

preprocessing used: 
augmentation used:
mosaic=1
mixup=1
blur=1
flip=1
OTWWWWW

# Training Tempo in Colab
![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619442644347_image.png)

![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619442667179_image.png)

![](https://paper-attachments.dropbox.com/s_3D1629D3D5877340AB13975E0EABFBF46D4E54D08FEEAF005AB18D2D3EF78954_1619442678996_image.png)



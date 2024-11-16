darknet:
	darknet detector demo Dataset\Crowdhuman\yolo_crowdhuman.data cfg\yolov4-custom-crowdhuman-3.cfg trained_models\fulltrained\CrowdHuman\yolov4\Training_3_[21_04_2021]\yolov4-custom-crowdhuman-3_last.weights Input\video1.mp4 -dont_show -ext_output > yolov4-custom-crowdhuman-3_fps.txt

darknet: 
	darknet detector demo Dataset\Crowdhuman\yolo_crowdhuman.data cfg\yolov4-custom-crowdhuman-tf-1.cfg trained_models\fulltrained\CrowdHuman\yolov4\Training_4_[24_04_2021]\yolov4-custom-crowdhuman-tf-1_last.weights Input\video1.mp4 -dont_show -ext_output > yolov4-custom-crowdhuman-tf-1_fps.txt

darknet:
	darknet detector demo Dataset\Crowdhuman\yolo_crowdhuman.data cfg\yolov4-custom-crowdhuman-tf-3.cfg trained_models\fulltrained\CrowdHuman\yolov4\Training_6_[25_04_2021]\yolov4-custom-crowdhuman-tf-3_last.weights Input\video1.mp4 -dont_show -ext_output > yolov4-custom-crowdhuman-tf-3_fps_1.txt

darknet:
	darknet detector demo Dataset\Crowdhuman\yolo_crowdhuman.data cfg\yolov4-custom-crowdhuman-vgg16-3.cfg trained_models\fulltrained\CrowdHuman\vgg16-yolov4\yolov4-custom-crowdhuman-vgg16-3_last.weights Input\video1.mp4 -dont_show -ext_output > yolov4-custom-crowdhuman-vgg16-3_fps_1.txt

darknet:
	darknet detector demo Dataset\Crowdhuman\yolo_crowdhuman.data cfg\yolov4-tiny-custom-crowdhuman-1.cfg trained_models\fulltrained\CrowdHuman\yolov4_tiny\Training_1_[30_03_2021]\yolov4-tiny-custom-crowdhuman-1_last.weights Input\video1.mp4 -dont_show -ext_output > yolov4-tiny-custom-crowdhuman-1_last_fps_1.txt

darknet:
	darknet detector map Dataset\Crowdhuman\yolo_crowdhuman.data cfg\yolov4-custom-crowdhuman-vgg16-3.cfg trained_models\fulltrained\CrowdHuman\vgg16-yolov4\yolov4-custom-crowdhuman-vgg16-3_last.weights -iou_thresh .75 > yolov4-custom-crowdhuman-vgg16-3_last_mAP75_last.txt

darknet:
	darknet detector map Dataset\Crowdhuman\yolo_crowdhuman.data cfg\yolov4-custom-crowdhuman-tf-4.cfg trained_models\fulltrained\CrowdHuman\yolov4\Training_8_[25_04_2021]\yolov4-custom-crowdhuman-tf-4_final.weights -iou_thresh .75 > yolov4-custom-crowdhuman-tf-4_mAP75.txt

darknet:
	darknet detector train Dataset/Crowdhuman/yolo_crowdhuman.data cfg/yolov4-custom-crowdhuman-effnet-3.cfg -dont_show -map > training_log.txt

darknet:
	darknet detector train Dataset/Crowdhuman/yolo_crowdhuman.data cfg/yolov4-custom-crowdhuman-effnet-3.cfg trained_models/yolov4-custom-crowdhuman-effnet-3_last.weights -dont_show -map > training_log.txt

darknet:
	darknet detector train Dataset/Crowdhuman/yolo_crowdhuman.data cfg/yolov4-custom-crowdhuman-resnext50-3.cfg -dont_show -map > training_log.txt

darknet:
	darknet detector map Dataset\Crowdhuman\yolo_crowdhuman.data cfg\yolov4-custom-crowdhuman-1.cfg trained\yolov4\Training_1_[23_03_2021]\yolov4-custom-crowdhuman-1_6000.weights -iou_thresh .75 > yolov4-custom-crowdhuman-1_6000_mAP75.txt

darknet:
	darknet detector map Dataset\Crowdhuman\yolo_crowdhuman.data cfg\yolov4-tiny-custom-crowdhuman-1.cfg trained\yolov4_tiny\Training_1_[30_03_2021]\yolov4-tiny-custom-crowdhuman-1_last.weights > yolov4-tiny-custom-crowdhuman-1_last_mAP50.txt

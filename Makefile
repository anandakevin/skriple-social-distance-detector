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

<<<<<<< HEAD
# Variables
DATA_DIR := data
TRAIN_DIR := $(DATA_DIR)/train
VALID_DIR := $(DATA_DIR)/valid
ANNOTATION_TRAIN := $(DATA_DIR)/annotation_train.odgt
ANNOTATION_VALID := $(DATA_DIR)/annotation_valid.odgt
SCRIPTS_DIR := scripts
PYTHON := python

# Target to generate annotations for the training set
generate_train_annotations:
	$(PYTHON) $(SCRIPTS_DIR)/generate_darknet_annotations.py --dataset train --annotation_file $(ANNOTATION_TRAIN)

# Target to generate annotations for the validation set
generate_valid_annotations:
	$(PYTHON) $(SCRIPTS_DIR)/generate_darknet_annotations.py --dataset valid --annotation_file $(ANNOTATION_VALID)

# Default target to generate both training and validation annotations
generate_all_annotations: generate_train_annotations generate_valid_annotations

clean_all_annotations:
	@echo "Cleaning up generated annotations..."
	rm -f $(TRAIN_DIR)/*_darknet.txt $(VALID_DIR)/*_darknet.txt $(DATA_DIR)/train.txt $(DATA_DIR)/valid.txt
=======
docker-build-darknet:
	docker build -t darknet:latest .
	
docker-push-darknet:
	docker push <your-registry>/darknet:latest

watch:
	watchmedo auto-restart --pattern="*.py" --recursive -- python controllers/sd_controller.py
>>>>>>> 838eb66 (wip: added CI/CD related configs)

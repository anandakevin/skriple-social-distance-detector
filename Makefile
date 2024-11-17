# Variables
DARKNET := darknet
DATASET := Dataset\Crowdhuman\yolo_crowdhuman.data
INPUT_VIDEO := Input\video1.mp4
TRAINING_LOG := training_log.txt

# Darknet commands
DETECTOR_DEMO := detector demo
DETECTOR_MAP := detector map
DETECTOR_TRAIN := detector train

# Commands
darknet_demo:
	$(DARKNET) $(DETECTOR_DEMO) $(DATASET) cfg\yolov4-custom-crowdhuman-3.cfg trained_models\fulltrained\CrowdHuman\yolov4\Training_3_[21_04_2021]\yolov4-custom-crowdhuman-3_last.weights $(INPUT_VIDEO) -dont_show -ext_output > yolov4-custom-crowdhuman-3_fps.txt

darknet_demo_tf_1:
	$(DARKNET) $(DETECTOR_DEMO) $(DATASET) cfg\yolov4-custom-crowdhuman-tf-1.cfg trained_models\fulltrained\CrowdHuman\yolov4\Training_4_[24_04_2021]\yolov4-custom-crowdhuman-tf-1_last.weights $(INPUT_VIDEO) -dont_show -ext_output > yolov4-custom-crowdhuman-tf-1_fps.txt

darknet_demo_vgg16_3:
	$(DARKNET) $(DETECTOR_DEMO) $(DATASET) cfg\yolov4-custom-crowdhuman-vgg16-3.cfg trained_models\fulltrained\CrowdHuman\vgg16-yolov4\yolov4-custom-crowdhuman-vgg16-3_last.weights $(INPUT_VIDEO) -dont_show -ext_output > yolov4-custom-crowdhuman-vgg16-3_fps_1.txt

darknet_demo_tiny:
	$(DARKNET) $(DETECTOR_DEMO) $(DATASET) cfg\yolov4-tiny-custom-crowdhuman-1.cfg trained_models\fulltrained\CrowdHuman\yolov4_tiny\Training_1_[30_03_2021]\yolov4-tiny-custom-crowdhuman-1_last.weights $(INPUT_VIDEO) -dont_show -ext_output > yolov4-tiny-custom-crowdhuman-1_last_fps_1.txt

darknet_map_vgg16:
	$(DARKNET) $(DETECTOR_MAP) $(DATASET) cfg\yolov4-custom-crowdhuman-vgg16-3.cfg trained_models\fulltrained\CrowdHuman\vgg16-yolov4\yolov4-custom-crowdhuman-vgg16-3_last.weights -iou_thresh .75 > yolov4-custom-crowdhuman-vgg16-3_last_mAP75_last.txt

darknet_map_tf_4:
	$(DARKNET) $(DETECTOR_MAP) $(DATASET) cfg\yolov4-custom-crowdhuman-tf-4.cfg trained_models\fulltrained\CrowdHuman\yolov4\Training_8_[25_04_2021]\yolov4-custom-crowdhuman-tf-4_final.weights -iou_thresh .75 > yolov4-custom-crowdhuman-tf-4_mAP75.txt

darknet_train_effnet:
	$(DARKNET) $(DETECTOR_TRAIN) Dataset/Crowdhuman/yolo_crowdhuman.data cfg/yolov4-custom-crowdhuman-effnet-3.cfg -dont_show -map > $(TRAINING_LOG)

darknet_train_effnet_resume:
	$(DARKNET) $(DETECTOR_TRAIN) Dataset/Crowdhuman/yolo_crowdhuman.data cfg/yolov4-custom-crowdhuman-effnet-3.cfg trained_models/yolov4-custom-crowdhuman-effnet-3_last.weights -dont_show -map > $(TRAINING_LOG)

darknet_train_resnext:
	$(DARKNET) $(DETECTOR_TRAIN) Dataset/Crowdhuman/yolo_crowdhuman.data cfg/yolov4-custom-crowdhuman-resnext50-3.cfg -dont_show -map > $(TRAINING_LOG)

darknet_map_yolov4:
	$(DARKNET) $(DETECTOR_MAP) $(DATASET) cfg\yolov4-custom-crowdhuman-1.cfg trained\yolov4\Training_1_[23_03_2021]\yolov4-custom-crowdhuman-1_6000.weights -iou_thresh .75 > yolov4-custom-crowdhuman-1_6000_mAP75.txt

darknet_map_tiny:
	$(DARKNET) $(DETECTOR_MAP) $(DATASET) cfg\yolov4-tiny-custom-crowdhuman-1.cfg trained\yolov4_tiny\Training_1_[30_03_2021]\yolov4-tiny-custom-crowdhuman-1_last.weights > yolov4-tiny-custom-crowdhuman-1_last_mAP50.txt
	
# Variables
DATA_DIR := data
TRAIN_DIR := $(DATA_DIR)/train
VALID_DIR := $(DATA_DIR)/valid
ANNOTATION_TRAIN := $(DATA_DIR)/annotation_train.odgt
ANNOTATION_VALID := $(DATA_DIR)/annotation_valid.odgt
SCRIPTS_DIR := scripts
PYTHON := python
LOG_FILE := processing.log  # Default log file path

# Target to generate annotations for the training set
generate_train_annotations:
	$(PYTHON) $(SCRIPTS_DIR)/generate_darknet_annotations.py --dataset train --annotation_file $(ANNOTATION_TRAIN) --log_file $(LOG_FILE)

# Target to generate annotations for the validation set
generate_valid_annotations:
	$(PYTHON) $(SCRIPTS_DIR)/generate_darknet_annotations.py --dataset valid --annotation_file $(ANNOTATION_VALID) --log_file $(LOG_FILE)

# Default target to generate both training and validation annotations
generate_all_annotations: generate_train_annotations generate_valid_annotations

clean_all_annotations:
	@echo "Cleaning up generated annotations..."
	rm -f $(TRAIN_DIR)/*_darknet.txt $(VALID_DIR)/*_darknet.txt $(DATA_DIR)/train.txt $(DATA_DIR)/valid.txt $(LOG_FILE)

docker-build-darknet:
	docker build -t darknet:latest .
	
docker-push-darknet:
	docker push <your-registry>/darknet:latest

watch:
	watchmedo auto-restart --pattern="*.py" --recursive -- python controllers/sd_controller.py

.PHONY: kustomize-darknet-dev
kustomize-darknet-dev:
	kustomize build k8s/final/staging > k8s/final/staging/argocd/staging-jakarta.yaml

.PHONY: kustomize-darknet-prod
kustomize-darknet-prod:
	kustomize build k8s/final/production > k8s/final/production/argocd/production-jakarta.yaml

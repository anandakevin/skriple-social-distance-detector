from ctypes import *
import math
import random
import os
import cv2
import sys
import numpy as np
import time
# import darknet
from itertools import combinations

max_number_of_crowd_count = 0
min_crowd_count_qualifier = 6
num_of_people_at_risk = 0
num_of_groups = 0
num_of_crowd = 0

def getMaxCrowdCount():
	global max_number_of_crowd_count
	return max_number_of_crowd_count

def getMinCrowdCountQualifier():
	global min_crowd_count_qualifier
	return min_crowd_count_qualifier

def returnInferenceResult():
	d = dict()
	d['num_of_people_at_risk'] = num_of_people_at_risk
	d['num_of_groups'] = num_of_groups
	d['num_of_crowd'] = num_of_crowd
	d['min_crowd_count_qualifier'] = min_crowd_count_qualifier
	d['max_crowd_count'] = max_number_of_crowd_count
	# print('d: ', d)
	return d

def resetVar():
	global max_number_of_crowd_count, min_crowd_count_qualifier, num_of_people_at_risk, num_of_groups, num_of_crowd
	max_number_of_crowd_count = 0
	min_crowd_count_qualifier = 6
	num_of_people_at_risk = 0
	num_of_groups = 0
	num_of_crowd = 0

class SocialDistanceDetector:
	def __init__(self):
		# self.min_x_distance = 50
		# self.min_y_distance = 15
		# self.min_distance = math.sqrt(self.max_x_distance**2 + self.max_y_distance**2)
		self.min_distance = 175
		self.crowdCount = 0

	def is_close(self, p1, p2):
		"""
		#================================================================
		# 1. Purpose : Calculate Euclidean Distance between two points
		#================================================================    
		:param:
		p1, p2 = two points for calculating Euclidean Distance

		:return:
		dst = Euclidean Distance between two 2d points
		"""
		dst = math.sqrt(p1**2 + p2**2)
		#=================================================================#
		return dst 


	def convertBack(self, x, y, w, h): 
		#================================================================
		# 2.Purpose : Converts center coordinates to rectangle coordinates
		#================================================================  
		"""
		:param:
		x, y = midpoint of bbox
		w, h = width, height of the bbox
		
		:return:
		xmin, ymin, xmax, ymax
		"""
		xmin = int(round(x - (w / 2)))
		xmax = int(round(x + (w / 2)))
		ymin = int(round(y - (h / 2)))
		ymax = int(round(y + (h / 2)))
		return xmin, ymin, xmax, ymax

	def cvDrawBoxes(self, detections, img):
    # , max_distance, min_crowd_count, max_number_of_crowd_count
	# print("Detections: ", detections) 
		"""
		:param:
		detections = total detections in one frame
		img = image from detect_image method of darknet

		:return:
		img with bbox
		"""
		global max_number_of_crowd_count, min_crowd_count_qualifier, num_of_people_at_risk, num_of_groups, num_of_crowd
		
		#================================================================
		# 3.1 Purpose : Filter out Persons class from detections and get 
		#           bounding box centroid for each person detection.
		#================================================================
		if len(detections) > 0:  						# At least 1 detection in the image and check detection presence in a frame  
			centroid_dict = dict() 						# Function creates a dictionary and calls it centroid_dict
			objectId = 0								# We inialize a variable called ObjectId and set it to 0
			for detection in detections:				# In this if statement, we filter all the detections for persons only
				# new
				detectionNew = (detection[0], float(detection[1]), detection[2])

				# Check for the only person name tag 
				name_tag = str(detectionNew[0])   # Coco file has string of all the names
				if name_tag == 'person':                
					x, y, w, h = detection[2][0],\
								detection[2][1],\
								detection[2][2],\
								detection[2][3]      	# Store the center points of the detections
					xmin, ymin, xmax, ymax = self.convertBack(float(x), float(y), float(w), float(h))   # Convert from center coordinates to rectangular coordinates, We use floats to ensure the precision of the BBox            
					# Append center point of bbox for persons detected.
					centroid_dict[objectId] = (int(x), int(y), xmin, ymin, xmax, ymax) # Create dictionary of tuple with 'objectId' as the index center points and bbox
					objectId += 1 #Increment the index for each detection      
		#=================================================================#
			# print('total people detected: ', len(centroid_dict))
			# print(centroid_dict)
		#=================================================================
		# 3.2 Purpose : Determine which person bbox are close to each other
		#=================================================================            	
			red_zone_list = [] # List containing which Object id is in under threshold distance condition. 
			red_line_list = []

			new_red_zone_list = dict()

			for (id1, p1), (id2, p2) in combinations(centroid_dict.items(), 2): # Get all the combinations of close detections, #List of multiple items - id1 1, points 2, 1,3
				dx, dy = p1[0] - p2[0], p1[1] - p2[1]  	# Check the difference between centroid x: 0, y :1

				distance = self.is_close(dx, dy) 			# Calculates the Euclidean distance
				firstIdx = -1
				secIdx = -1
				if distance < self.min_distance:
					print("dx:", dx, ', dy:', dy, ', dist:', distance, ', danger')
				else:
					print("dx:", dx, ', dy:', dy, ', dist:', distance, ', safe')
				if distance < self.min_distance:				# Set our social distance threshold - If they meet this condition then..
					for ids in new_red_zone_list:
						if id1 in new_red_zone_list[ids] and firstIdx == -1:
							firstIdx = ids
						if id2 in new_red_zone_list[ids] and secIdx == -1:
							secIdx = ids
						if firstIdx != -1 and secIdx != -1:
							break

					# print(id1, ' ', id2, ' ', firstIdx, ' ', secIdx)

					if firstIdx != -1 and secIdx != -1 and firstIdx != secIdx: 
						new_red_zone_list[min(firstIdx, secIdx)] = new_red_zone_list[firstIdx] + new_red_zone_list[secIdx]
						del new_red_zone_list[max(firstIdx, secIdx)]
					elif firstIdx != -1:
						if id2 not in new_red_zone_list[firstIdx]:
							new_red_zone_list[firstIdx].append(id2)
					elif secIdx != -1:
						if id1 not in new_red_zone_list[secIdx]:
							new_red_zone_list[secIdx].append(id1)
					else:
						new_red_zone_list[len(new_red_zone_list)] = [id1, id2]

					# print("red_zone_list", red_zone_list)
					# print("new_red_zone_list", new_red_zone_list)

					red_line_list.append(p1[0:2])
					red_line_list.append(p2[0:2])

					if id1 not in red_zone_list:
						red_zone_list.append(id1)       #  Add Id to a list
						# red_line_list.append(p1[0:2])   #  Add points to the list
					if id2 not in red_zone_list:
						red_zone_list.append(id2)		# Same for the second id 
						# red_line_list.append(p2[0:2])

			for idx, box in centroid_dict.items():      # dict (1(key):red(value), 2 blue)  idx - key  box - value
				if idx in red_zone_list:   # if id is in red zone list
					cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (255, 0, 0), 2) # Create Red bounding boxes  #starting point, ending point size of 2
				else:
					cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (0, 255, 0), 2) # Create Green bounding boxes << format: RGB
					# cv2.rectangle(image, start_point, end_point, color, thickness)
			#=================================================================#

			# print("Final Result: ", new_red_zone_list)
			#=================================================================
			# 3.3 Purpose : Display Risk Analytics and Show Risk Indicators
			#=================================================================
			num_of_people_at_risk = len(red_zone_list)
			num_of_groups = len(new_red_zone_list)
			self.crowdCount = 0

			ttlRedPeople = "People at Risk: %s" % str(num_of_people_at_risk) 			# Count People at Risk
			ttlGroup = "Number of groups at risk: %s" % str(num_of_groups)
			
			# print("red_zone_list ", red_zone_list)
			# print("new_red_zone_list", new_red_zone_list)
			for idx in new_red_zone_list:
				# print('idx:', idx)
				# print('new_red_zone_list[idx]:', new_red_zone_list[idx])
				# print("jumlah orang: ", len(new_red_zone_list[idx]), ", orang2nya: ", new_red_zone_list[idx])
				if len(new_red_zone_list[idx]) >= min_crowd_count_qualifier:
					# print('crowdCount:', self.crowdCount)
					self.crowdCount += 1
			# print("crowdCount: ", crowdCount)

			ttlCrowd = "Number of crowd consisting of at least %s people: %d" % (str(min_crowd_count_qualifier), self.crowdCount)
			max_number_of_crowd_count = max(self.crowdCount, max_number_of_crowd_count)
			maxNumberOfCrowdCount = "Max Number of crowd consisting of at least %s people: %d" % (str(min_crowd_count_qualifier), max_number_of_crowd_count)

			location1 = (10,25)												# Set the location of the displayed text
			location2 = (10,60)												# Set the location of the displayed text
			location3 = (10,95)												# Set the location of the displayed text
			location4 = (10,130)												# Set the location of the displayed text

			cv2.putText(img, ttlRedPeople, location1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4, cv2.LINE_AA)  # Display Text
			cv2.putText(img, ttlRedPeople, location1, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)  # Display Text

			cv2.putText(img, ttlGroup, location2, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4, cv2.LINE_AA)  # Display Text
			cv2.putText(img, ttlGroup, location2, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)  # Display Text

			cv2.putText(img, ttlCrowd, location3, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4, cv2.LINE_AA)  # Display Text
			cv2.putText(img, ttlCrowd, location3, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)  # Display Text

			cv2.putText(img, maxNumberOfCrowdCount, location4, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4, cv2.LINE_AA)  # Display Text
			cv2.putText(img, maxNumberOfCrowdCount, location4, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)  # Display Text

			# print(red_line_list)
			for check in range(0, len(red_line_list)-1):					# Draw line between nearby bboxes iterate through redlist items
				start_point = red_line_list[check] 
				end_point = red_line_list[check+1]
				check_line_x = abs(end_point[0] - start_point[0])   		# Calculate the line coordinates for x  
				check_line_y = abs(end_point[1] - start_point[1])			# Calculate the line coordinates for y
				# if (check_line_x < max_x_distance) and (check_line_y < max_y_distance):				# If both are We check that the lines are below our threshold distance.
				if (self.is_close(check_line_x, check_line_y) < self.min_distance):				# If both are We check that the lines are below our threshold distance.
					cv2.line(img, start_point, end_point, (255, 0, 0), 2)   # Only above the threshold lines are displayed. 
				# (Red, Green, Blue, Line Thickness)
			#=================================================================#
		return img, num_of_people_at_risk, num_of_groups, self.crowdCount



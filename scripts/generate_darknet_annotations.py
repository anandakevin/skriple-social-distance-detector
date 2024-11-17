import os
import yaml
import cv2
import argparse
from multiprocessing import Process, Manager
from tqdm import tqdm

# Constants
intPERSON = 0
intHEAD = 1

def generate_annotations(ii, return_dict, dataset_path, annotation_file):
    line = return_dict[ii]
    del return_dict[ii]
    
    dictLine = yaml.load(line, Loader=yaml.FullLoader)  # Safe loading with FullLoader

    strID = dictLine['ID']

    # Build the file path based on the dataset and image ID
    img_path = os.path.join(dataset_path, 'images', f'{strID}.jpg')
    img = cv2.imread(img_path, 1)

    imgWidth = img.shape[1]
    imgHeight = img.shape[0]

    # Create .txt label file for Darknet format
    output_txt_path = os.path.join(dataset_path, 'annotations', f'{strID}_darknet.txt')
    with open(output_txt_path, 'w+') as txtf:

        for label in dictLine['gtboxes']:
            # Skip labels that should be ignored or are unsure
            if 'extra' in label and ('ignore' in label['extra'] and label['extra']['ignore'] == 1):
                continue
            if 'extra' in label and ('unsure' in label['extra'] and label['extra']['unsure'] == 1):
                continue 

            # Process person bounding box (fbox)
            px = float(label['fbox'][0])
            py = float(label['fbox'][1])
            pw = float(label['fbox'][2])
            ph = float(label['fbox'][3])

            # Process head bounding box (hbox)
            hx = float(label['hbox'][0])
            hy = float(label['hbox'][1])
            hw = float(label['hbox'][2])
            hh = float(label['hbox'][3])

            # Normalize the bounding boxes
            # Person BB
            cpx = px + pw / 2
            cpy = py + ph / 2
            abspx = cpx / imgWidth
            abspy = cpy / imgHeight
            abspw = pw / imgWidth
            absph = ph / imgHeight  

            abspx = 1 if abspx > 1 else abspx
            abspy = 1 if abspy > 1 else abspy
            abspw = 1 if abspw > 1 else abspw
            absph = 1 if absph > 1 else absph
            abspx = 0.000001 if abspx < 0 else abspx
            abspy = 0.000001 if abspy < 0 else abspy
            abspw = 0.000001 if abspw < 0 else abspw
            absph = 0.000001 if absph < 0 else absph

            # Head BB
            chx = hx + hw / 2
            chy = hy + hh / 2
            abshx = chx / imgWidth
            abshy = chy / imgHeight
            abshw = hw / imgWidth
            abshh = hh / imgHeight  

            abshx = 1 if abshx > 1 else abshx
            abshy = 1 if abshy > 1 else abshy
            abshw = 1 if abshw > 1 else abshw
            abshh = 1 if abshh > 1 else abshh
            abshx = 0.000001 if abshx < 0 else abshx
            abshy = 0.000001 if abshy < 0 else abshy
            abshw = 0.000001 if abshw < 0 else abshw
            abshh = 0.000001 if abshh < 0 else abshh

            # Write normalized bounding boxes to file in Darknet format
            txtf.write(f'{intPERSON} {abspx:.4f} {abspy:.4f} {abspw:.4f} {absph:.4f}\n')
            txtf.write(f'{intHEAD} {abshx:.4f} {abshy:.4f} {abshw:.4f} {abshh:.4f}\n')

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Generate Darknet annotations.')
    parser.add_argument('--dataset', type=str, required=True, help='Path to the dataset directory (train or valid).')
    parser.add_argument('--annotation_file', type=str, required=True, help='Path to the annotation file.')
    args = parser.parse_args()

    dataset_path = os.path.join('data', args.dataset)  # Assuming 'data' is the project root
    annotation_file = args.annotation_file

    # Initialize the multiprocessing manager and shared dictionary
    manager = Manager()
    return_dict = manager.dict()

    # Read the annotation file and add to the shared dictionary
    with open(annotation_file) as f:
        processes = []
        max_iter = 500  # Define max iterations before joining processes

        for ii, line in tqdm(enumerate(f)):
            return_dict[ii] = line  # Add annotation line to return_dict
            p = Process(target=generate_annotations, args=(ii, return_dict, dataset_path, annotation_file))
            processes.append(p)
            p.start()

            if ii % max_iter == 0:
                # Join processes in batches to avoid too many simultaneous processes
                for jj in range(len(processes)):
                    processes[jj].join()
                processes = []

        # Join any remaining processes
        for jj in range(len(processes)):
            processes[jj].join()

if __name__ == '__main__':
    main()

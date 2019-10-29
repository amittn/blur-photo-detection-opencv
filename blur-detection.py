from imutils import paths, contours
import cv2
import json
import os
import argparse
import numpy as np

class Arguments:
    show_image: True
    images_dir: ''
    run_blur_test: True
    output_results_file: True

class Results:
    blur_score: 'N/A'
    file_name: ''

# https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
def variance_of_laplacian(image):   
	# focus measure of the image using the Variance of Laplacian method
	# load the image, convert it to grayscale, and compute the
    # Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	return cv2.Laplacian(image, cv2.CV_64F).var()

def showImage(image, result):
    window_name = result.file_name
    base_pixel_size = 600
    height, width = image.shape[:2]
  
    cv2.putText(image, "Blur score: {}".format(result.blur_score), (10, 100),
		cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
    
    cv2.namedWindow(window_name,  cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL )

    if (height > width):
        cv2.resizeWindow(window_name, base_pixel_size , int(height * (base_pixel_size / width)))
    else:
        cv2.resizeWindow(window_name, int(width * (base_pixel_size / height)), base_pixel_size)
    
    cv2.imshow(window_name, image)
    key = cv2.waitKey(0)
        
    if (key == 113 or key == 27):
        # exit is q or ESC is pressed
        exit()

def parseArguments():
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--images", required=True,
            help="path to input directory of images")
    ap.add_argument("-s", "--show-image", required=True, type=bool,
        help="whether to show the image on screen")
    ap.add_argument("-t", "--tests", nargs="+", choices=['blur'], required=True,
        help="Tests to runs.  Can be one of \"blur\" ...")
    ap.add_argument("-o", "--output-result-file", required=False, default=True,
        help="Whether to output the results to a file")
    
    args = vars(ap.parse_args())
    
    result = Arguments()
    result.images_dir = args["images"]
    result.show_image = args["show_image"]
    result.run_blur_test = "blur" in args["tests"]
    result.output_results_file = args["output_result_file"]
    return result

def main():
    args = parseArguments()
    image_path = args.images_dir
    output_file = None

    try:
        if args.output_results_file:
            output_file = open("results.json", "w")

        for imagePath in paths.list_images(image_path):
            image = cv2.imread(imagePath)
            result = Results()
            result.blur_score = variance_of_laplacian(image)
            result.file_name = image_path
            
            if args.show_image:
                showImage(image, result)
            
            if args.output_results_file:
                output_file.write(json.dumps(result.__dict__))
                output_file.write('\n')
    finally:
        if output_file is not None:
            output_file.close()

# Run
main()



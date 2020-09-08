import csv
import cv2
import pathlib
import logging
import os
import sys
from datetime import datetime

# Processing pair of images from a single row in the input file in tab delimited csv format.
# The similarities and processing time for each row are stored in an output file in tab delimited csv format.
# As per user requirements, fully matched images will ouput 0.0 where fully unmatched images will output 1.0.
# Arguments : {input file path, output file path)
# Note --> Changing allowed extensions of an image: hasValidImageExtension method
# Note --> Changing allowed headers of input file: check_invalidfileheaders method
# Note --> User requested matching values: similar_value method

# Note --> Must required after each modification to run unit test associated with the script. 
#     -->  For any logic changes in the previous notes, the tests are required to be changed.  
class ImageDiffer:
    def __init__(self, inputFile, outputFile):
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.file_info = {} #Cache for image description
        logging.basicConfig(filename='app.log', filemode='w', 
                            format='%(name)s - %(levelname)s - %(message)s') #logging in app.log file


    # Checking valid extension for an image.
    def hasValidImageExtension(self, filepath):
        valid_ext = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'] #allowed extensions
        return filepath.lower().endswith(tuple(valid_ext))


    # Retrieving an image property (description in formal language).
    def getImageDesc(self, filepath):
        try:
            image = cv2.imread(filepath)
        except cv2.error as e:
            return False, str(e)

        orb = cv2.ORB_create()
        ignore, desc = orb.detectAndCompute(image, None)
        return True, desc


    # Calculating similarites between two images based on number of matches of image propoerties 
    # in similar regions from two images.
    # Output 
    #    Fully matched      --> 1.0
    #    Fully unmatched    --> 0.0
    #    Paritially matched --> 0.0 < X < 1.0
    def sift_sim(self, image_1, image_2):
        # checking images have valid extension and their file path do exist or not.
        if not self.hasValidImageExtension(image_1) or not os.path.exists(image_1):
            return False, "Invalid image " + image_1
        if not self.hasValidImageExtension(image_2) or not os.path.exists(image_2):
            return False, "Invalid image " + image_2
       
        # For two images with same file path:
        if image_1 == image_2:
            return True, 1.0

        #Caching images description in {file_info} dict for images encounterd more than one occassion.
        if image_1 in self.file_info:
            desc_1 = self.file_info[image_1]
        else:
           success, desc_1 = self.getImageDesc(image_1)
           if not success:
               return desc_1
           self.file_info[image_1] = desc_1
        
        if image_2 in self.file_info:
            desc_2 = self.file_info[image_2]
        else:
           success, desc_2 = self.getImageDesc(image_2)
           if not success:
               return desc_2
           self.file_info[image_2] = desc_2

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
        matches = bf.match(desc_1, desc_2)
        
        similar_regions = [i for i in matches if i.distance < 70]

        if len(matches) == 0:
            return True, 0.0
        else:
            return True, len(similar_regions) / len(matches)


    # Converting similarity values as per user requirement. 
    # Output 
    #    Fully matched      --> 0.0
    #    Fully unmatched    --> 1.0
    #    Paritially matched --> 0.0 < X < 1.0 (No conversion is performed)
    def similar_value(self, val):
        assert val >= 0 and val <= 1.0
        if val == 0.0 or val == 1.0:
            return 1.0 - val
        return val

    # Checking validity of the header in the input file. 
    def check_invalidfileheaders(self, headers):
        valid_headers = ['Image_1', 'Image_2'] #allowed headers
        return len(headers) != 2 or headers[0] != valid_headers[0] or headers[1] != valid_headers[1]

    # Algorithm to process an input file.
    # 1. Read a single row from the input File
    # 2. Find similarities between two images from that row
    # 3. Calculate time required to process that row
    # 3.a Store in a list after converting the similarities as per user requirement
    # 4. Store the list to the output file
    def process(self): 
        try:
            # Counting number of process row for logging purpose. 
            row = 1
            with open(self.inputFile, "r") as file:
                reader = csv.DictReader(file, delimiter='\t')
                # Ensuring headers of the input file is not invalid. 
                if self.check_invalidfileheaders(reader.fieldnames):
                    print("Input file has invalid header")
                    print("Correct headers for a file are Image_1 and Image_2")
                    return

                storeList = []
                for image_row in reader:
                    row += 1

                    assert len(image_row) == 2

                    image_1 = image_row['Image_1']
                    image_2 = image_row['Image_2']

                    startTime = datetime.now().timestamp()

                    # 1. Calculating similarites between two images. 
                    success, msg = self.sift_sim(image_1, image_2)
                    if not success:
                        logging.error("Line number " + str(row - 1) + ": " +  msg)
                        continue

                    # If calculation is succedded, <msg> at this point must be a floating point number. 
                    assert isinstance(msg, float)
                    
                    endTime = datetime.now().timestamp()
                    # 2. Time required to calculate the difference.
                    elapse = endTime - startTime

                    # 3. Storing the values to a list which will be later stored in the output file. 
                    tmp_list = []
                    tmp_list.append(image_row['Image_1'])
                    tmp_list.append(image_row['Image_2'])
                    # 3.a Converting similar value according to the user requriement
                    tmp_list.append(str(self.similar_value(msg)))
                    tmp_list.append(str(elapse))
                    storeList.append(tmp_list)

        except Exception as e:
            print("Failed to process input file: " + self.inputFile)
            print("caused by exception: " + str(e))

        try:
           # 4. Storing the list to the output file.  
           with open(self.outputFile, "w") as o:
                file_writer = csv.writer(o, delimiter='\t')
                file_writer.writerow(['IMAGE1','IMAGE2','SIMILAR','ELAPSE'])
                o.writelines('\t'.join(i) + '\n' for i in storeList)
        
        except Exception as e:
            print("Failed to store results in output file: " + self.outputFile)
            print("caused by exception: " + str(e))



if __name__ =='__main__':
    if len(sys.argv) != 3:
        print ('missing arguments')
        print ('valid arguments: [input].csv, [output].csv')
        exit(0)

    diff = ImageDiffer(sys.argv[1], sys.argv[2]) 
    diff.process()

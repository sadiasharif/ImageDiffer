# ImageDiffer:
ImgaeDiffer is a Python based script for calculating the difference of visual apperances between a pair of images, read from provided input file.
The script results in similarity value and processing time for a single pair of images.

# Similarity Values:
    Fully Match       -->  0.0
    Fully Unmatched   -->  1.0
    Partially Matched  --> 0.0 < X < 1.0
    
 To find similraties, sift comparison algorithm is used as it provides better results.   
 https://stackoverflow.com/questions/50217364/sift-comparison-calculate-similarity-score-python?fbclid=IwAR1zsr2zmZ-dNTXwaNBM0emluPVlO-GORYikMijy5Dc7gQSZvlKlWwqK_FQ

 In summary, at first exact matches and similar regions are identified from two image's descriptive properties. Later, these values are used to calculate similarity. 

# Usage:
 Run command:   
 python3 Image_Differ.py <Input.csv> <Output.csv>

 The script requires user to provide Input file, containing list of pair of images, and Output file in CSV format.   
 The header of the Input.csv must be only 'Image_1' and 'Image_2'.  
 Each row of the Input file must contain two images with valid extensions.   
 Valid Image files must have one of these extensions: JPEG, JPG, PNG, BMP, GIF, TIFF.  
 Output file should contain:  
 IMAGE1 IMAGE2  SIMILARITY  ELAPSED

# Enviornment:
  # Linux: 
  Install any version of Python >= 3:   
          apt install python3
          
  # Windows:
  Install any version of Python >= 3 by installing Anaconda Package from below:  
         https://www.anaconda.com/products/individual#windows    
       
# Running test:
 Run command:  
  python3 ImageDiffer_Unittest.py 

  Four test cases are expected to run and show results.  
  Note: Three images associated with the script must not be deleted to run the test.
  
# Log File:
  The script generates error detailed logs for images it cannot process and stores in "app.log" file in the same directory of the script.    
  Each line of the log file states the row number from the input file, it failes to process.  

# Note:
  The process is optimized with caching description of a single image as there is a possibility of same image will be encountered multiple times. This could effectively 
  reduce time elapsed for calculating similraties of that pair. Also, multiple pair of iamges can be processed parallelly by introducing multiple threads. However, this would   definitely provide not correct processing time for a pair.  



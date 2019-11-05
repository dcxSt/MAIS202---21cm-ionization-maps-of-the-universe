
# imports
import numpy as np
import os
import sys
from google.colab import drive
drive.mount('/content/drive')
sys.path.append('./drive/My Drive/')
sys.path.append('./drive/My Drive/mais_project/')

# helper methods for the pre-processing


# Takes a 'category' which is a substring of some of the box files that identifies that file as belonging to
# a certain type of data. 
# Also takes a unique identifier for a file in a given category, this is a substring of the filename that
# only appears in this file.
# This function returns a box of data read from the file
def get_bin21(filename_includes , category_includes , mypath):
    fnames = filenames_in(mypath)
    category = [i for i in fnames if category_includes in i]
    print("there are ",len(category),"files in the category "+category_includes)# trace

    filename = [i for i in category if filename_includes in i]
    if len(filename)!= 1: raise Exception("Error the number of files that match your description is no 1\n it is "+str(len(filename)))

    filename = filename[0]
    
    return binary_to_3dbox(mypath+filename)

# helper method for the above method
def binary_to_3dbox(file):
    f_21cm = open(file,"rb")
    binary_21cm = f_21cm.read()
    np_float_array_21cm = np.fromstring(binary_21cm , np.float32)
    f_21cm.close()

    return np.reshape(np_float_array_21cm , (200,200,200))

# helper for above, returns list of filenames in mypath
def filenames_in(mypath="./joelle_batch_2.1/joelle_ESC_FRAC_0.070_RNG_150/"):
    filenames = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]
    return filenames

# takes two boxes and saves a bunch of matching picutres to a files w/ specified names in specified directory
def save_to_2d_arrays(data_mass , data_ion , dir_path="./matching_pictures/" , fname_suffix="matching"):
    small_boxes = []
    for data_box in [data_mass , data_ion]:
        # first cut the data into 64 smaller boxes 50 x 50 x 50
        for i in range(64):
            small_boxes.append(data_box[50* (i%4):50* (i%4+1),
                50* int(i/4.%4):50* (int(i/4.%4)+1),
                50* int(i/16.%4):50* (int(i/16.%4)+1)])

        #print([i.shape for i in small_boxes[0].shape])# trace
        print("shape of boxes:",small_boxes[0].shape)#trace

    # now we reshape the small_boxes and couple the mass / ionization maps
    small_boxes_new = []
    print(len(small_boxes) / 2)# check this is even
    r = int(len(small_boxes)/2)# should be 64
    for i in range(r):
        small_boxes_new.append([small_boxes[i],small_boxes[i+r]])
    small_boxes = np.array(small_boxes_new)

    print("small_boxes.shape:",small_boxes.shape)# trace

    # now cut up the small boxes into a bunch of matching pictures
    # save to directory

    count = 0
    for small_box in small_boxes:
        mass_box = small_box[0]
        ion_box = small_box[1]
        for i in range(len(mass_box)):
            mass_slice = mass_box[i]
            ion_slice = ion_box[i]
            matching_slices = np.array([mass_slice , ion_slice])

            fname = fname_suffix+"_"+str(count)+"_"+str(i)+".npy"
            np.save(dir_path+fname , matching_slices)
        count +=1
        print(count , end=" ")# trace


# Method that takes a redshift value as input, finds the block with this 
# redshift value in ESC FRAC 0.070, cuts it up into slices and saves these 
# in it's own folder in ES_FRAC_delta_T_slices
# The variable redshift is a string that looks something like "z0.01300"
def save_images_ESC_FRAC_0070(redshift, over_write=False):
  # get a list of the names of the files in "joelle_ESC_FRAC_0.070_RNG_150/"
  mypath = "./drive/My Drive/21cmFAST_bank/joelle_batch_2.1/joelle_ESC_FRAC_0.070_RNG_150/"
  save_path = './drive/My Drive/mais_project/ESC_FRAC_delta_T_slices/'
  fnames = pm.filenames_in(mypath = mypath)
  delta_T_fnames = []
  
  for f in fnames:
    if "delta_T" in f: delta_T_fnames.append(f)
  # find the individual filename
  fname = []
  for f in delta_T_fnames: 
    if redshift in f: fname.append(f)
  if len(fname) != 1: raise Exception("the redshift value is not unique!")
  fname = fname[0]
  
  # get the data from the file
  data_delta_T = pm.binary_to_3dbox(mypath + fname)
  
  # make a directory where you will save the data for the box if there isn't one there already
    
  dir_name = "ESC_FRAC_delta_T_redshift_"+str(redshift)
  if not os.path.exists(save_path + dir_name):
    os.makedirs(save_path + dir_name)
  
  else:
    if over_write==False:
      print("There is already a directory here, the files will not be over-written")
      print("Set 'over-write' to True if you wish to over-write the files in this directory")
      return
  
  # cut up the 200^3 box into 64 50^3 boxes
  small_boxes = []
  for i in range(64):
    small_boxes.append(data_delta_T[50* (i%4):50* (i%4+1),
                               50* int(i/4. %4):50* (int(i/4. %4)+1),
                               50* int(i/16. %4):50* (int(i/16.%4)+1)])
    
  # check that the boxes are all the same shape
  the_shape = small_boxes[0].shape
  for i in small_boxes: 
    if i.shape != the_shape: 
      raise Exception('the small boxes are not the same shape! '+str(the_shape)+' vs '+str(i.shape))
  print("shape of boxes:",the_shape)# trace
  
  # cut up the small boxes into 2d arrays and save them as numpy arrays
  print("Saving the boxes")
  for i in range(len(small_boxes)):
    box = small_boxes[i]
    for j in range(len(box)):
      fname = "ESC_FRAC_0.070_RNG_150_"+str(i).zfill(2)+"_"+str(j).zfill(3)+".npy"# 3 and not 2 just in case i want to re-cycle for bigger arrays
      one_slice = box[j]
      np.save(save_path+dir_name+"/"+fname , one_slice)
      
  print("all slices from redshift\n"+dir_name+"/ are saved")  
   


def save_all_ESC_FRAC_0070():
    # make list of redshifts to save
    redshifts_to_save = []
    redshift = 5.0
    while redshift <= 13:
        redshifts_to_save.append("z"+str(int(redshift)).zfill(3)+"."+str(redshift)[-1:]+"0")
        redshift += 0.5
    print(redshifts_to_save)

    # save the redshifts
    for redshift in redshifts_to_save:
        print(redshift, end="...\n")
        save_images_ESC_FRAC_0070(redshift , over_write=False)




def print_files_0070():
    files = [f for f in os.listdir("./drive/My Drive/21cmFAST_bank/joelle_batch_2.1/joelle_ESC_FRAC_0.070_RNG_150/")]
    files.sort()
    for f in files:
	print(f)






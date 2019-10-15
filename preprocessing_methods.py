
# imports
import numpy as np
import os


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




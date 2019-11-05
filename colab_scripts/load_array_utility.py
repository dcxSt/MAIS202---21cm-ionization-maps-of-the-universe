
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
  
 
def print_esc_frac(esc_frac_value=0.070):
  as_string = str(esc_frac_value)
  if len(as_string)==4: 
    as_string = as_string+"0"
  files = [f for f in os.listdir("./drive/My Drive/21cmFAST_bank/joelle_batch_2.1/joelle_ESC_FRAC_"+esc_frac_value+"_RNG_150/")]
  files.sort()
  for f in files: 
    print(f)
  return files














import numpy as np
def binary_to_3dbox(file):
    f_21cm 				= open(file, "rb")
    binary_21cm 		= f_21cm.read()
    np_float_array_21cm = np.fromstring(binary_21cm, np.float32)
    f_21cm.close()

    #return one slice 
    return np.reshape(np_float_array_21cm, (200,200,200))

    #return full 3d box
    # return np_float_array_21cm

def main():
    #saves one slice of 3d box
    filename = input()
    box = binary_to_3dbox(filename)
    np.savetxt(filename + '.txt', box[:,0], delimiter=',')

if __name__ == "__main__":
    main()

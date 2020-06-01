import sys
import cv2
import numpy as np
import traceback



from src.label 				import Label, lwrite
from os.path 				import splitext, basename, isdir
from os 					import makedirs
from src.utils 				import crop_region, image_files_from_folder
#import darknet.python.darknet as dn
#from darknet.python.darknet import detect
#from YOLO3_4_Py.pydarknet import Detector, Image
from pydarknet import Detector, Image


if __name__ == '__main__':

	try:
		
		input_dir  = sys.argv[1]
		output_dir = sys.argv[2]
		
       
		vehicle_threshold = .5

                #vehicle_weights = 'data/vehicle-detector/yolo-voc.weights'.encode('ascii')
                #vehicle_netcfg  = 'data/vehicle-detector/yolo-voc.cfg'.encode('ascii')
                #vehicle_dataset = 'data/vehicle-detector/voc.data'.encode('ascii')
                #vehicle_net  = dn.load_net(vehicle_netcfg, vehicle_weights, 0)
                #vehicle_meta = dn.load_meta(vehicle_dataset)
		vehicle_weights = bytes('YOLO3_4_Py/weights/yolov3.weights',encoding="utf-8")
		vehicle_netcfg  = bytes('YOLO3_4_Py/cfg/yolov3.cfg',encoding="utf-8")
		vehicle_dataset = bytes('YOLO3_4_Py/cfg/coco.data',encoding="utf-8")
	
		vehicle_net  = Detector(vehicle_netcfg, vehicle_weights,0, vehicle_dataset)
		#vehicle_meta = dn.load_meta(vehicle_dataset)
	
		imgs_paths = image_files_from_folder(input_dir)
		imgs_paths.sort()

		if not isdir(output_dir):
			makedirs(output_dir)

		print ('Searching for vehicles using YOLO...')
	
		for i,img_path in enumerate(imgs_paths):

			print ('\tScanning %s' % img_path)

			bname = basename(splitext(img_path)[0])

			#R,_ = detect(vehicle_net, vehicle_meta, img_path ,thresh=vehicle_threshold)
			f_image=cv2.imread(img_path)
			f_image2=Image(f_image)
			t= vehicle_net.detect(f_image2)
			print("2")
			print(t)
			quit()

			R = [r for r in R if r[0] in ['car','bus']]

			print ('\t\t%d cars found' % len(R))

			if len(R):

				Iorig = cv2.imread(img_path)
				WH = np.array(Iorig.shape[1::-1],dtype=float)
				Lcars = []

				for i,r in enumerate(R):

					cx,cy,w,h = (np.array(r[2])/np.concatenate( (WH,WH) )).tolist()
					tl = np.array([cx - w/2., cy - h/2.])
					br = np.array([cx + w/2., cy + h/2.])
					label = Label(0,tl,br)
					Icar = crop_region(Iorig,label)

					Lcars.append(label)

					cv2.imwrite('%s/%s_%dcar.png' % (output_dir,bname,i),Icar)

				lwrite('%s/%s_cars.txt' % (output_dir,bname),Lcars)

	except:
		traceback.print_exc()
		sys.exit(1)

	sys.exit(0)
	

import os
import boto
from glob import glob
import helpers as h
 
'''
To run:
python upload_images_to_s3.py --bucket_name drawbase-demo --path_to_imgs photodraw2

'''

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--bucket_name', type=str, help='name of S3 bucket?', \
		default='drawbase-demo')
	parser.add_argument('--path_to_imgs', type=str, help='path to images to upload?', \
		default='./photodraw2')   
	args = parser.parse_args()

	## tell user some useful information
	print 'Path to images is : {}'.format(args.path_to_imgs)    
	print 'Uploading to this bucket: {}'.format(args.bucket_name)

	## establish connection to s3 
	conn = boto.connect_s3()

	## create a bucket with the appropriate bucket name
	try: 
		b = conn.create_bucket(args.bucket_name) 
	except:
		b = conn.get_bucket(args.bucket_name) 

	## establish path to image data
	path_to_img = args.path_to_imgs

	## get list of image paths
	all_files = h.list_files(path_to_img,ext='jpg')

	## now loop through image paths and actually upload to s3 
	for i,a in enumerate(all_files):
		imname = a.split('/')[-1]
		print 'Now uploading {} | {} of {}'.format(a,i,len(all_files))
		try:
			k = b.new_key(imname) ## if we need to overwrite this, we have to replace this line boto.get_key
		except:
			k = b.get_key(imname)
		k.set_contents_from_filename(a)
		k.set_acl('public-read')
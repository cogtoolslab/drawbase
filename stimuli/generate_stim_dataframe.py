from __future__ import division
import os
import numpy as np
import pandas as pd
import json
import pymongo as pm
import helpers as h

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--path_to_imgs', type=str, help='path to images to upload?', \
		default='./photodraw2') 	
	parser.add_argument('--bucket_name', type=str, help='name of bucket on S3 images are hosted in', \
		default='drawbase-demo')
	parser.add_argument('--dataset_name', type=str, help='name of dataset to store in stimuli db', \
		default='photodraw2')		
	args = parser.parse_args()

	## specify custom experiment params here
	conditions = ['photo','label'] # some trials are photo-cued, some are label-cued

	## source path
	path_to_img = args.path_to_imgs

	## bucket name and dataset name
	bucket_name = args.bucket_name
	dataset_name = args.dataset_name	

	## get list of image paths
	image_paths = h.list_files(path_to_img,ext='jpg')

	## generating dataframe for each image (photo and label cue versions)
	print('Generating dataframe with each cue and their attributes...')    
	condition = [] # photo vs. label
	category = [] 
	image_id = []
	image_url = []
	games = [] # this field keeps track of which games this triplet has been shown in
	shuffler_ind = []

	## generate permuted list of triplet indices in order to be able retrieve from triplets pseudorandomly
	inds = np.arange(len(conditions)*len(image_paths)) 
	shuffled_inds = np.random.RandomState(0).permutation(inds)
	counter = 0
	for cond_ind,this_condition in enumerate(conditions):
		for im_ind,this_img in enumerate(image_paths):  
			condition.append(this_condition)
			category.append(this_img.split('/')[-2])
			_image_id = this_img.split('/')[-1].split('.')[0]
			image_id.append(_image_id)
			image_url.append('https://s3.amazonaws.com/{}/{}.jpg'.format(bucket_name,_image_id))
			games.append([])
			shuffler_ind.append(shuffled_inds[counter])
			counter += 1  

	## Generating pandas dataframe...
	print('Generating pandas dataframe...') 
	table = [condition,category,image_id,image_url,games,shuffler_ind]
	headers = ['condition','category','image_id','image_url','games','shuffler_ind']
	df = pd.DataFrame(table)
	df = df.transpose()
	df.columns = headers

	## save out to file
	print('Saving out json dictionary out to file...') 
	stimdict = df.to_dict(orient='records') 
	with open('{}_meta.js'.format(dataset_name), 'w') as fout:
		json.dump(stimdict, fout)	

	### next todo is to upload this JSON to initialize the new stimulus collection
	print('next todo is to upload this JSON to initialize the new stimulus collection...')
	import json
	J = json.loads(open('{}_meta.js'.format(dataset_name),mode='ru').read())

	assert len(J)==len(image_paths)*len(conditions)
	print 'dataset_name: {}'.format(dataset_name)
	print 'num entries in stim dictionary: {}'.format(len(J))	

	## remember to establish tunnel to mongodb on remote server first

	# set vars 
	auth = pd.read_csv('auth.txt', header = None) # this auth.txt file contains the password for the sketchloop user
	pswd = auth.values[0][0]
	user = 'sketchloop'
	host = 'rxdhawkins.me' ## cocolab ip address

	# have to fix this to be able to analyze from local
	conn = pm.MongoClient('mongodb://sketchloop:' + pswd + '@127.0.0.1')
	db = conn['stimuli']
	coll = db[dataset_name]	

	## actually add data now to the database (iff collection is empty)
	if coll.count()==0:
		print('Uploading data')
		for (i,j) in enumerate(J):
			if i%10==0:
				print ('%d of %d' % (i,len(J)))
			coll.insert_one(j)	
	else:
		print('Collection {} is not empty. Will not upload and overwrite now.'.format(dataset_name))

import os
import shutil

fullFileList = []
dir_name = os.getcwd()

for root, dirs, files in os.walk(".", topdown=False):
	for name in files:
		fullFileList.append(
				os.path.realpath(				#get absolute directory from relative directory
					os.path.join(root, name)	#return relative directory of the form ./dirname/filename
				)
			)

for files in fullFileList:
	if files.endswith(".pdf"):	#get only the files that end with .pdf
		shutil.move(files, 
					dir_name + '\\pdfs\\' + os.path.split(files)[1]
					)
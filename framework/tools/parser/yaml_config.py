############################################################################ 
# 
#  Copyright 2017 
# 
#   https://github.com/HPC-buildtest/buildtest-framework
# 
#  This file is part of buildtest. 
# 
#    buildtest is free software: you can redistribute it and/or modify 
#    it under the terms of the GNU General Public License as published by 
#    the Free Software Foundation, either version 3 of the License, or 
#    (at your option) any later version. 
# 
#    buildtest is distributed in the hope that it will be useful, 
#    but WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#    GNU General Public License for more details. 
# 
#    You should have received a copy of the GNU General Public License 
#    along with buildtest.  If not, see <http://www.gnu.org/licenses/>. 
############################################################################# 


"""
Function that process the YAML config and verify key/value.
Also declares the valid YAML keys that can be used when writing YAML configs


:author: Shahzeb Siddiqui (Pfizer)
"""

import os
import sys
import yaml 


field={
	'name':'',
	'source':'',
	'envvars':'',
	'args':'',
	'scheduler':['SLURM','LSF','PBS'],
	'buildopts':'',
	'buildcmd':'',
	'inputfile':'',
	'iter':'',
	'outputfile':'',
	'runcmd':'',
	'runextracmd':'',
	'mpi':'enabled',
	'cuda':'enabled',
	'nproc': '',
	'threadrange':'',
	'procrange':'',
	'jobslots':'',
	
}

def parse_config(filename,codedir):
	"""
	read config file and verify the key-value content with dictionary field
	"""
        fd=open(filename,'r')
	content=yaml.load(fd)
	# iterate over dictionary to seek any invalid keys 
	for key in content:
		if key not in field:
			print "ERROR: invalid key", key 
			sys.exit(1)
		# key-value name must match the yaml file name, but strip out .yaml extension for comparison
		if key == "name":
			strip_ext=os.path.splitext(filename)[0]
        	        # get name of file only for comparison with key value "name"
                	testname=os.path.basename(strip_ext)
                	if content[key] != testname:   
                        	print "Invalid value for key: ",key,":",content[key],". Value should be:", testname
				sys.exit(1)
		if key == "mpi":
			if content[key] != "enabled":
				print "Error processing YAML file: ", filename
				print """ "mpi" key must take value "enabled" """
				sys.exit(1)
		# source must match a valid file name
		if key == "source" or key == "inputfile":
	                codefile=os.path.join(codedir,content[key])
        	        if not os.path.exists(codefile):
                	        print "Can't find source file: ",codefile, ". Verify source file in directory:", codedir
				sys.exit(1)
		# checking for invalid scheduler option
		if key == "scheduler":
			if content[key] not in field["scheduler"]:
				print "Invalid scheduler option: ", key, " Please select on of the following:" , field["scheduler"]
				sys.exit(1)
		if key == "nproc" or key == "iter" or key =="jobslots":
			# checking whether value of nproc and iter is integer
			if not str(content[key]).isdigit(): 
				print key + " key must be an integer value"
				sys.exit(1)
			# checking whether key is negative or zero
			else:
				if int(content[key]) <= 0: 
					print key + " must be greater than 0"
					sys.exit(1)
		if key == "procrange" or key == "threadrange":
			# format procrange: 2,10,3
			if len(content[key].split(",")) != 3:
				print "Error processing YAML file: ", filename
				print "Format expected: <start>,<end>,<interval> i.e 4,40,10"
				sys.exit(1)

			startproc = content[key].split(",")[0]
			endproc = content[key].split(",")[1]
			procinterval = content[key].split(",")[2]
			if not startproc.isdigit():
				print "Error in ", filename, " expecting integer but found",  startproc
				sys.exit(1)

			if not endproc.isdigit():
				print "Error in ", filename, " expecting integer but found",  endproc
				sys.exit(1)

			if not procinterval.isdigit():
				print "Error in ", filename, " expecting integer but found",  procinterval
				sys.exit(1)


		
			
	fd.close()
	return content


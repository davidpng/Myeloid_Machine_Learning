<h1>README</h1>
<p>
AUTHOR: David Ng, MD
	University of Washington
	Department of Laboratory Medicine
DATE:	17 September 2014

/Input_Outputs/Comp_libs 
This folder contains spectral overlap coefficents for the various flow tubes - T-cell tube not collected yet

These are python classes accessed through Main.py that will:

1 find FCS files according to a case list and file structure (HEADER_FIND_FCS_files.py)
2 Read in uncompensated FCS files (HEADER_Import_FCS.py)
3 Bins FCS files and outputs cases (sets of FCS files) as a sparse row matrix (HEADER_ND_Binning.py)
4 Saves these results (and metadata) to an HDF5 file as follows (HEADER_Generate_HDF5.py):
</p>
'''
	/tube/<case num>/tube1
			 tube2
                         tube3

        /data/<case num>/data
                        /indices
                        /indptr
                        /shape
	n.b.: The saved elements in data are sufficent to regenerated a scipy.sparse.csr_matrix data stucture
'''
<p>
HEADER_Read_FCS.py
Defines a class that handles reading of the HDF5 file.
Work in progress
</p>

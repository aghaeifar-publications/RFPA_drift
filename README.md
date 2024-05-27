
# RFPA Drift Correction
Scripts used to extract DICO values from rawdata and compute the correction factors to compensate RFPA drift. 

### Requirements:
The tool is tested under Python 3.10 with the following package installed:

 - numpy
 - twixtools ([+](https://github.com/pehses/twixtools))

### Scripts:
The **dico_tools.py** script provides two functions for extracting DICO values from raw data:

1) `read_dico(twixObj)`: This function retrieves all samples from both the forward and reflected signals. Note that using this function requires sufficient available and free memory.

usage:
```bash
file_path = 'path_to_rawdata.dat'
twixObj  =  twixtools.read_twix(file_path)
forward, reflect = dico_tools.read_dico(twixObj)
```
`forward` and `reflect` represent lists of NumPy arrays, where each element in the list, a NumPy array, corresponds to a distinct RF object. When referring to an RF object, we denote various types of RF within the sequence, such as excitation or saturation. These RF objects are differentiated by their respective durations, distinguishing one from another.


2) `read_dico_memOpt(twixObj)`: Alternatively, this function calculates the integral of absolute values from the forward signal. It is specifically designed to work efficiently with huge raw data, offering memory optimization.

usage:
```bash
file_path = 'path_to_rawdata.dat'
twixObj  =  twixtools.read_twix(file_path)
forward, rf_length = dico_tools.read_dico_memOpt(twixObj)
```
`forward` comprises a list of NumPy arrays, each containing the integral of absolute values derived from the forward signal. `rf_length` is a Python list, providing the duration of RF objects in us.

These functions offer different approaches for extracting dico values, allowing you to choose the one that best suits your memory requirements and the size of your raw data. In our approach, the calculation of correction factors ultimately relies on the integration of the forward signal. 

### 
The **predictive_correction.py** calculate correction factor and save the factors into a text file.
usage:
```bash
chmod +x predictive_correction.py
./predictive_correction path_to_rawdata.dat
```
### Citation:
Please refer to the following publication for citation of this work:

https://doi.org/10.1002/mrm.30078

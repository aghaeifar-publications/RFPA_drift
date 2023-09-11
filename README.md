# RFPA drift correction
Scripts used for correcting RFPA drift 

The **dico_tools** library provides two functions for extracting dictionary values from raw data:

1. `read_dico(twixObj)`: This function retrieves all samples from both the forward and reflected signals. It is important to note that using this function requires sufficient available and free memory.

2. `read_dico_memOpt(twixObj)`: Alternatively, this function calculates the integral of absolute values from the forward signal. It is specifically designed to work efficiently with huge raw data, offering memory optimization.

These functions offer different approaches for extracting dico values, allowing you to choose the one that best suits your memory requirements and the size of your raw data. In our approach, the calculation of correction factors ultimately relies on the integration of the forward signal. Therefore, we are currently utilizing the `read_dico_memOpt(twixObj)` function.

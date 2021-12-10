This folder contains the code and data from the article: Constraint Based Evaluation of Generalisation, Even with Raster Maps?
The code is organized as follow:

- File constraints.py contains the code for each constraint measures.
- File utils.py contains some utils functions for calculating measures.
- File test.py contains the instructions to calculate the constraints on the test data and register the measure in a csv.

The data are organized as follow:
- Folder real contains detailed images of mountain roads extracted from the alps and those generalisations.
- Folder seg contains the associated roads masks. 

The first letter of the image name represent the generalisation method:
- i: not generalised
- c: generalised using cycleGAN
- p: generalised using pix2pix
- u: generalised using U-Net
- r: the reference generalisation (GALBE)  

# dynamic-motion-digitset
A Data Collection Mechanism that will allow us to collect dynamic motion handwritten digits

Overview:
---------
**Version:** v2.2

**Data Version:** v1.0



#### The Main Files:

- *main.py* contains the main code for data collection. Run this to use the data collection program.
- *predict.py* contains the main code for the prediction window. Run this to use the live data prediction tool.
  - This file loads alternative modules from the *prediction* folder and looks for a pre-trained model file (ending with *.hdf5*)



##### Notice:

Due to the little time I had left, I stopped updating the documentation since v2.0

I hope that the git commit history may help shed some light on the changes I made.

As a consequence, the prediction window is completely undocumented, but the GUI portion of the code is entirely based on the data collection code. In addition it utilizes the libraries used in the data tools code in my second repository dynamic-motion-data-tools. 

To understand better the live prediction tool (Prediction Window), consider look through the other repository dynamic-motion-data-tools that's purpose is to analyse and build a neural network based on the data you collect with the code in this repository.

One more important thing to note, is that although collected "Digitset" data can be packed into a "Dataset", the other repository makes no use of this and instead deals with files saved as separate "Digitsets".

For privacy reasons, I omitted the collected data from the repository. If you wish to repeat the research you will have to collect your own dataset.
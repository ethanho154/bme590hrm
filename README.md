# BME590 Heart rate monitor assignment
In this assignment we are writing a python script which can take ECG data from a csv file and find various attributes of the data using an object-oriented approach. In my implementation, 3 different python scripts were used.

## data_reader
data_reader was a simple script which consisted of the ecg_reader object which only has 1 input, a string of the csv file name. It would take in a csv file, organize the data through a pandas dataframe, and then convert everything to floats. This would also truncate any lost data. Once this was done, the data is ready to be analyzed.

## data_analyzer
data_analyzer was the bulk of this project. Calling upon data_reader, the ecg_reader class takes in two inputs, the file name which it inputs into ecg_reader and the number of segments the sample should be broken into. The critical information we were trying to obtain from the ECG were the mean heart rate beats per minute, the voltage extremes, duration of the ECG, number of beats, and when they occurred. The time between each heartbeat was found via autocorrelation. The number of segments the user specified in the beginning determined how many segments would be autocorrelated with each other to find underlying patterns which would reveal information about heart rate and heart beats.

## main
This third script was a simple one, almost a counterpart to the data_reader (honestly I should have just called it data_writer but I was planning on doing more with but couldn't in the sake of time). It would import in the ecg_analyzer object, and thus it had two inputs, the file name and number of segments. Once calling ecg_analyzer, it would then call all the data obtained from it and load it into a json file.

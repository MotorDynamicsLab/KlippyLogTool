



# Installation instructions



## python environment installation



**python installation: Download version 3.9.0**.

**Dependency installation: run pip install -r requirements.txt to install dependent packages**.

**Python run main_view.py to run it **.





## Run it directly (you can download the release file directly to run it)



Unzip the zip file and run AnalyseLog.exe directly.





# Basic operations



## Set analysis interval

You can set the intervals of the x-axis to be analysed. **The results will be different for different intervals, and if you set the interval too large, you may not be able to see some details of the waveforms.**

![image-20240902143143741](./img/image-20240902143143741.png)



## Select Hide/Show Line



Click on the target in the way box to choose to hide/show the target line segments

![image-20240902144944322](./img/image-20240902144944322.png)



# Related issues





## Meaning of x-axis

The x-axis is the line spacing in the stats file



![image-20240822101753771](./img/image-20240822101753771.png)





Its value * sampling interval is the number of lines in the stats file. As shown below 100`*`100=5000, i.e. 50 is the 10000th line in the stats file.

![image-20240902143306123](./img/image-20240902143306123.png)







## Determining the moment of disconnection

A spike like the one in the picture below is basically a break.

![image-20240902143403815](./img/image-20240902143403815.png)





## Analyse the error for that position in the diagram



Click Packet Loss Analysis to copy an error message

![](./img/image-20240902143424564.png)


Open the current log and stats files

![image-20240902143442520](./img/image-20240902143442520.png)





Search for the error message in the log, find the basis stats before the error, and copy the

![image-20240902143528597](./img/image-20240902143528597.png)





Search from the stats file to find the corresponding line as follows

![image-20240902143544132](./img/image-20240902143544132.png)



From this, we know that the location of row 9100 is approximately at the following location, as follows (91*100 = 9100)

![image-20240902143631964](./img/image-20240902143631964.png)

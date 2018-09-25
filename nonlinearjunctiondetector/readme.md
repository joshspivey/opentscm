# SDR Non Linear Junction Detector 

Needs full duplex SDR that goes to at least 6ghz
The SDR GNU radio version is modeled after the nljd PDF file

https://web.wpi.edu/Pubs/E-project/Available/E-project-011518-172228/unrestricted/Final_Report.pdf

Make sure you install gr-fosphor, gr-sdr

You have to add you full duplex device address in the source and the sink

##### todo: 

1. Make PCB design for antenna "Needs a PCB log antenna that goes from 10hz to 6ghz"
2. Needs a script to show it detected something right now it completes the loop in the histogram
3. Needs requirements.txt
4. Needs cross platform X11 references to work on mac and windows. Right now will work on linux in the cli or you need gnu radio companion installed and run the GRC.


##### Howto find the device address:
```
> SoapySDRUtil --find
> ######################################################
> ## Soapy SDR -- the SDR abstraction library
> ######################################################

> Found device 0
>   addr = 241:1204
>   driver = lime
>   media = USB
>   module = STREAM
>   name = USB 3.0 (Stream)
```


####################################################################

# DIY Hardware Non Linear Junction Detector

http://67.225.133.110/~gbpprorg/mil/non/index.html
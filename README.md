# SENSEMATE

This project's objective is to design a iot based smart accessory that can be worn with any regular dresscode and using a Deep Learning based model to detect for any possible human presence. This device aims to ensure the safety of the visually impaired person by alerting them for any nearby human presence. 

By using a local Deep Learning model for the detection along with the companion android application we can ensure good data management and user experience. 


## IOT Components

1. ESP-32 CAM Module
2. Buck converter
3. Rechargable AA batteries 


## Face Detection Methodology

By utilizing a CNN based Deep Learning model to detect possible human presense from the images captured with the ESP-32 Cam module placed in position from where it can easily cover most of the field of vision of the user. 

The model architecture is located in face_detector.ipynb file in the main branch. 

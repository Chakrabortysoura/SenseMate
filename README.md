
# SENSEMATE

This project's objective is to design a iot based smart accessory that can be worn with any regular attire and using a Deep Learning based model to detect for any possible human presence. This device aims to ensure the safety of the visually impaired person by alerting them for any nearby human presence. 

 
## PROJECT OVERVIEW

"Esp32-CAM Ai thinker" module is the main iot component which when placed at a suitable place like attached to a hat or used attached as an accessory it can easily take pictures from the perspective of the user. These real time image capture is then sent to the companion mobile application for postprocessing. Along with some very basic post-procesing to the image the image is analized by the Deep learning model to detect any human possibly nearby to alert the user and the image is then saved for future use along with date and timestamp.

## IOT Components

1. ESP-32 CAM Module
2. Buck Converter
3. Rechargable 18650 batteries Li ion batteries
4. TP4056 cgarging ckt

## case holder



## Face Detection Methodology

By utilizing a CNN based Deep Learning model to detect possible human presense from the images captured with the ESP-32 Cam module placed in position from where it can easily cover most of the field of vision of the user. 

The model architecture is located in face_detector.ipynb file in the main branch. 


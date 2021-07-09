# Custom Vision + Azure IoT Edge on a Raspberry Pi 3


This is a sample showing how to deploy a Custom Vision model to a Raspberry Pi 3 device running Azure IoT Edge. Custom Vision is an image classifier that is trained in the cloud with your own images. IoT Edge gives you the possibility to run this model next to your cameras, where the video data is being generated. You can thus add meaning to your video streams to detect road traffic conditions, estimate wait lines, find parking spots, etc. while keeping your video footage private, lowering your bandwidth costs and even running offline.

## Prepare development environment. 

1. You should have the following prerequisites in place:

    - A free or standard-tier IoT Hub in Azure.
    - A device running Azure IoT Edge with Linux containers. You can use the [quickstarts to set up a Linux device](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux?view=iotedge-2020-11) device.
    - A container registry, like [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/?view=iotedge-2020-11).
    - [Visual Studio Code](https://code.visualstudio.com/) configured with the [Azure IoT Tools](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-tools).
    - [Docker CE](https://docs.docker.com/install/) configured to run Linux containers.

1. To develop an IoT Edge module with the Custom Vision service, install the following additional prerequisites on your development machine:

    - Python (https://www.python.org/downloads/)
    - Git (https://git-scm.com/downloads)
    - Python extension for Visual Studio Code (https://marketplace.visualstudio.com/items?itemName=ms-python.python)


## Create a new Custom Vision model. 

1. In your web browser, navigate to the Custom Vision web page.  Sign in and sign in with the same account that you use to access Azure resources then create a new project for object detection.

1. The project set up and train described in the [tutorial](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/get-started-build-detector)

1. Be aware you need to use **compact** domain to be abele to export model for RPi.

1. Images for training can be find in the "Images" folder of this repository.

1. Train the model and test the model on any custom images. Details described in the [tutorial](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/test-your-model)

1. Export model as **Docker** file in [zip format](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/export-your-model#export-your-model)

1. Extract files from archive to the folder **modules\classifier** but do not override `app.py` and `Dockerfile`

## Build project


## Prepare RPi to Host IotEdge


## Deploy modules on RPi


## Monitor and diagnose application.


# References

1. [How to run object detection with Tensorflow 2 on the Raspberry PI using Docker](https://spltech.co.uk/how-to-run-object-detection-with-tensorflow-2-on-the-raspberry-pi-using-docker/)

1. [Build RPi solution from Ch9](https://github.com/Azure-Samples/Custom-vision-service-iot-edge-raspberry-pi)

1. [How To Access the Raspberry Pi Camera Inside Docker and OpenCV](https://spltech.co.uk/how-to-access-the-raspberry-pi-camera-inside-docker-and-opencv/)

1. [Fixing Docker build issue](https://dev.to/kenakamu/export-custom-vision-model-to-raspberry-pi-3-issue-and-fix-29bg)

1. [Uncompleted MS tutorial: Perform image classification at the edge with Custom Vision Service](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-deploy-custom-vision?view=iotedge-2020-11)

1. [Connection PI camera to RPi](https://www.teachmemicro.com/uploading-camera-images-raspberry-pi-website/)
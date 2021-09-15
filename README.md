# Custom Vision + Azure IoT Edge on a Raspberry Pi 3


This is a sample showing how to deploy a Custom Vision model to a Raspberry Pi 3 device running Azure IoT Edge. Custom Vision is an image classifier that is trained in the cloud with your own images. IoT Edge gives you the possibility to run this model next to your cameras, where the video data is being generated. You can thus add meaning to your video streams to detect road traffic conditions, estimate wait lines, find parking spots, etc. while keeping your video footage private, lowering your bandwidth costs and even running offline.

The project consists of the custom vision model deployed on Raspberry PI and detecting objects visible through the camera. 
![schema](/docs/schema.png)

## Toolbox.

- RPi 3 or 4 with power adapter
- External Camera or RPi camera.
- LAN or WiFi access.
- USB Keyboard.
- HDMI cable.
- HDMI Monitor. 
- Objects for detection (eg fruits).
- Laptop with VS code and docker.
- Azure Subscription (Free trial works). 

## Prepare development environment. 

1. You should have the following prerequisites in place:

    - A free or standard-tier IoT Hub in Azure.
    - A container registry, like [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/?view=iotedge-2020-11).
    - [Visual Studio Code](https://code.visualstudio.com/) configured with the [Azure IoT Tools](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-tools).
    - [Docker CE](https://docs.docker.com/install/) is configured to run Linux containers.

1. To develop an IoT Edge module with the Custom Vision service, install the following additional prerequisites on your development machine:

    - Python (https://www.python.org/downloads/)
    - Git (https://git-scm.com/downloads)
    - Python extension for Visual Studio Code (https://marketplace.visualstudio.com/items?itemName=ms-python.python)


## Create a new Custom Vision model. 

1. In your web browser, navigate to the Custom Vision web page.  Sign in and sign in with the same account that you use to access Azure resources then create a new project for object detection.

1. The project set up and train described in the [tutorial](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/get-started-build-detector).

1. Be aware you need to use a **compact** domain to be able to export models for RPi.

1. Images for training can be found in the "Images" folder of this repository.

1. Train the model and test the model on any custom images. Details described in the [tutorial](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/test-your-model).

1. Export model as **Docker** file in zip format as explained in the [tutorial](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/export-your-model#export-your-model).

1. Extract files from archive to the folder **modules\classifier** but do not override `app.py` and `Dockerfile`.



## Build project

1. Make sure in VS Code you select `arm32v7` as target platform.

1. Update .evn file in root folder with blob account details where analyzed files should be uploaded and credential for Azure Container Registry.

```ini
CONTAINER_REGISTRY_USERNAME=<your acr short name>
CONTAINER_REGISTRY_PASSWORD=4nKYmt8m=<your acr user password>
BLOB_ACC=<blob account short name>
BLOB_KEY=<blob account key>
```

1. From terminal window in VS Code run command to sign in `az acr login -n <short name of your ACR>`.

1. From terminal run command `py version.py` to generate new versions of the `module.json` files.

1. Select file `deployment.template.json` in project view and from context menu choice `Build and Push IoT Edge Solution`. Then docker builds images and pushes them in ACR. 

> First time building takes up to 20 min. You can proceed with RPi preparation while waiting for the build.

1. In case of the pillow error follow the proposed [fix](https://dev.to/kenakamu/export-custom-vision-model-to-raspberry-pi-3-issue-and-fix-29bg).

1. Make sure the build ends up successfully and your Azure Container Registry has required container images.

    ![ACR](/Docs/acr.png)


## Prepare RPi to Host Iot Edge

1. Download and flash the latest Raspbian image from the [official web site](https://www.raspberrypi.org/software/operating-systems/). Lite version without desktop will be a vise choice. For flashing SD cards you can use [Etcher](https://www.balena.io/etcher/).

1. Start RPi and run configuration [raspi-config](https://www.raspberrypi.org/documentation/computers/configuration.html) to allow SSH, camera access and network access. You need to connect the monitor and keyboard to complete configuration.

1. Connect by SSH to RPi (PuTTY) and change the default password.

1. For testing USB cameras you need to install `fswebcam` as explained in the following [tutorial](https://tutorials-raspberrypi.com/raspberry-pi-security-camera-with-webcam/). Then you can use `fswebcam` to take a snapshot. You can use WinSCP to connect to the RPi and download images to observe.

1. In case of the Pi Camera you can follow the [tutorial](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera) and use Python code to test. 

1. Before install IoT Edge you first need to install the container engine by executing the following commands in the [tutorial](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-install-iot-edge?view=iotedge-2020-11#install-a-container-engine).

1. You also need to install [IoT Edge](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-install-iot-edge?view=iotedge-2020-11#install-iot-edge) on your RPi device.

1.To properly configure `/etc/aziot/config.toml` you need to register your IoT device in Iot Hub. The following [tutorial](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-register-device?view=iotedge-2020-11&tabs=azure-portal) explained the registration process with a symmetric key. From the Azure portal create an IoT Hub and add a new Iot Edge device. Provide a unique name and keep all default settings and generated keys. Copy primary key into `config.toml`. 

1. Restart your device and wait for status update of device on the IoT Hub. You also can execute command "iotedge list" to monitor process. Please pay attention for the version of `azureiotedge-hub` and `azureiotedge-agent`you use. Version 1.0.0 having an issue and you can update that to version 1.2.2. You can use runtime settings as explained in following [tutorial](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-update-iot-edge?view=iotedge-2020-11&tabs=windows#update-a-specific-tag-image)   

1. Finlay you should have your IoTEdge modules running on RPi without errors. 
    
    ![output](/Docs/iothub-screen.png)



## Deploy modules on RPi

1. Make sure your build is successful and ACR contains the version you set up in configuration.

1. From the VS code context menu select command `Build and Publish Iot Edge Solution`. Then you can use command palette `Azure IoT Edge: Create deployment for a single device` and choose your device and file `config\deployment.arm32v7.json`.

>If you lost with deployment follow the steps in [tutorial](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-deploy-custom-vision?view=iotedge-2020-11#deploy-modules-to-device)

1. As result of deployment your RPi should contain 4 modules (`azureiotedge-agent`, `azureiotedge-hub`, `camera-capture`, `classifier`). You can monitor modules from IoT Hub or from the SSH console by command `iotedge list`. Remember that some images are quite heavy and require time to be downloaded from ACR to PI.


## Setting up the scene

1. Left the objects for identification on the solid background with about 3 fit distance from the camera.The blurry images will be unrecognizable.

    ![setup example](/Docs/PiCamSetUp-sm.png)

1. Make sure that there are enough lights in the picture area. 

1. You can also use the camera's tool on the Pi to take a few snapshots of objects and deploy images to the Custom vision and tag them to train better models.

    ![real image](/Docs/camera-taken.png)

## Monitor and diagnose applications.

1. From the SSH console you can use commands like `iotedge logs camera-capture` or `iotedge logs classifier` to monitor errors and issues. Correct output of the classifier should looks as following:

    ![output](/Docs/rp-result.png)

1. The `camera-capture` module is hosting a local web site on port **5052**. You can access it to monitor current camera setup. The image is updated once in a minute..

    ![local website](/Docs/fruits-sm.png)

1. Finlay if the classification is completed successfully the boundaries will be created on the image and analyzed images will be uploaded to the storage account you set up above.

    ![analyzed](/Docs/analyzed-group.png)


# References

1. [How to run object detection with Tensorflow 2 on the Raspberry PI using Docker](https://spltech.co.uk/how-to-run-object-detection-with-tensorflow-2-on-the-raspberry-pi-using-docker/)

1. [Build RPi solution from Ch9](https://github.com/Azure-Samples/Custom-vision-service-iot-edge-raspberry-pi)

1. [How To Access the Raspberry Pi Camera Inside Docker and OpenCV](https://spltech.co.uk/how-to-access-the-raspberry-pi-camera-inside-docker-and-opencv/)

1. [Fixing Docker build issue](https://dev.to/kenakamu/export-custom-vision-model-to-raspberry-pi-3-issue-and-fix-29bg)

1. [Uncompleted MS tutorial: Perform image classification at the edge with Custom Vision Service](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-deploy-custom-vision?view=iotedge-2020-11)

1. [Connection PI camera to RPi](https://www.teachmemicro.com/uploading-camera-images-raspberry-pi-website/)
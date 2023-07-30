# VDSC
Vision-based Fall Detection System for Senior Citizens using Computer Vision on Microcontroller

## 🔨 Usage
For Fall Detection
* open **https://ai-training.glitch.me/**
* connect with your microbit and make sure you uploaded the main microbit code.
* place **https://teachablemachine.withgoogle.com/models/Poit12UMC/** on the square frame.
* choose your camera
* click on **Ready!**

For Person Tracking
* preparation
```bash
pip install pipenv
```
* installation
```bash
git clone https://github.com/Kanapats/VDSC.git
cd VDSC/tracking/
pipenv shell
pipenv install
```
* before run make sure you connect microbit with your computer and uploaded the controller_vdsc microbit code.
```bash
python main.py
```

For the main microbit board.
* open [https://makecode.microbit.org/](https://makecode.microbit.org/)
* click on **New Project**
* click on **Extensions** under the gearwheel menu
* search for **https://github.com/kanapats/main_vdsc** and import
* and upload to your microbit.

For the microbit board that controls the robotic arm.
* open [https://makecode.microbit.org/](https://makecode.microbit.org/)
* click on **New Project**
* click on **Extensions** under the gearwheel menu
* search for **https://github.com/kanapats/controller_vdsc** and import
* and upload to your microbit.

For the microbit board that controls the speakers and the lights.
* open [https://makecode.microbit.org/](https://makecode.microbit.org/)
* click on **New Project**
* click on **Extensions** under the gearwheel menu
* search for **https://github.com/kanapats/component_vdsc** and import
* and upload to your microbit.

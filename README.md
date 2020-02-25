# autopilot

Starter template for the AutoPilot self-driving software. 

The package can be installed locally on the RPi by cloning your repository:

```
git clone https://github.com/<LINK_TO_YOUR_REPO>
```

then installing within the repo directory:

```
cd autopilot
sudo pip3 install .
```

Once autopilot has been installed, you will need to reboot the RPi to restart the webserver.

```
sudo reboot
```

After rebooting turn your car off and on again.

Please clone your repository in the home area of the Pi, and make sure to delete it afterwards and uninstall your package:

```
sudo pip3 uninstall autopilot
``` 

## Modifying

Most of your modifications will be made within autopilot/autopilot.py. 

Currently, it simply sets the speed to 30 and a straight steering angle. Your machine learning model should determine these values. 

```
# !! Use machine learning to determine angle and speed (if necessary - you may decide to use fixed speed) !!
    
speed = 30
angle = self.front_wheels._straight_angle

# !! End of machine learning !!
``` 

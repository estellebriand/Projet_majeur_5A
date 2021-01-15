# Projet de majeure "Robotique de service"
s5_g7_briand_guy_kahan_martinez

**Auteurs:** Estelle BRIAND_Nicolas GUY_Jeremie KAHAN_Paul MARTINEZ

# Useful Documentation

https://medium.com/robotics-with-ros/installing-the-rplidar-lidar-sensor-on-the-raspberry-pi-32047cde9588

https://www.youtube.com/watch?v=Qrtz0a7HaQ4

https://www.youtube.com/watch?v=qNdcXUEF7KU&ab_channel=RoboticsWeekends

http://smartroom.metz.supelec.fr/ArchiveCartoTurtlebot/Projet_turtlebot.html

| Goal | Status |
| ------ | ------ |
| Mapping Lidar | DONE |
| Ultrason RaspberryPi | DONE |
| Communication IHM/Lidar | Doing |
| IMU | TODO |

# ---------------------------------------------------------------------------------------
# Tuto: How to implement a RPLidar on RaspberryPi 3B+ using ROS

##### Robot Project - CPE Lyon 2020 / 2021
###
### Created by Nicolas Guy on Mon 11/02/2021


This tutorial will show you how to implement a RPLidar on a RasberryPi 3B+ using ROS. All the test have been done on Ubuntu 18.04 and ROS Kinetic. 

Setting used:
  - Ubuntu 18.04
  - ROS Kinetic
  - Catkin

### What is a RP Lidar ?
> RPLIDAR is a low cost 2D LIDAR solution developed by RoboPeak Team, SlamTec company. It canscan 360° environment within 6 meter radius. The output of RPLIDAR is very suitable to build map, do slam, or build 3D model.

### First step how to connect the RPLidar ?

Find a micro USB Cable and stick it in the USB port. Then connect the "5 cables" from the Lidar to the microcontroller hub. Finally, connect the USB cable to the RaspberryPi 3B+.

### Prepare your Ros Worspace and package

### Installation

```sh 
mkdir rplidar_ws
cd rplidar_ws
mkdir src
cd src
sudo git clone https://github.com/Slamtec/rplidar_ros.git
cd ~/rplidar_ws/
catkin_make
```
The build can take a lot of time, be patient and don't do anything during the catkin_make

After that, you have to source your bashrc with this command
```
source devel/setup.bash
```

### Activate the serial USB port

You need to activate the serial USB port of your RaspberryPi 3B+ for being able to connect the Lidar via USB. To do this your need to write the command:

```
sudo chmod 666 /dev/SERIAL_USED
```

To find the serial you are using you can use this command below. Most of the time it is ttyUSB0

```
ls -l /dev|grep ttyUSB
```

### Time to run the Lidar:

You just have to run the launcher you downloaded on the github from Slamtec and you should have your first mapping. (It is preferable to start a roscore on another terminal before)

    roslaunch rplidar_ros view_rplidar.launch
    
  - rpllidar_ros is the package
  - view_rplidar.launch is the launcher

At this point you should have Rviz running, the Lidar moving and your first mapping on Rviz.

# ---------------------------------------------------------------------------------------

#  Tuto: How to use SLAM with a RPLidar on RaspberryPi 3B+ using ROS

This tutorial is going to show you how to use SLAM with a RPLidar connected to a RaspberryPi 3B+ and ROS to have a better mapping of the environment. 

##### Robot Project - CPE Lyon 2020 / 2021
###
### Created by Nicolas Guy on Mon 11/02/2021

Setting used:
  - Ubuntu 18.04
  - ROS Kinetic
  - Catkin
  - RaspberryPi 3B+

### Have a look to the topic /scan

>To manage to do it you need to have completed the tutorial: How to implement a RPLidar on RaspberryPi 3B+ using ROS)

Let's first have a look to the topics that we have when we launch the view_rplidar.launch. To do that, open a terminal and go on your rplidar workspace. (It is preferable to start a roscore on another terminal before)

```
source devel/setup.bash
roslaunch rplidar_ros view_rplidar.launch
```

Open an other terminal, and use the rostopic echo command to see the topics used. The one that interest us the most is the /scan topic

```
rostopic echo /scan
```

You should see a bunch of numbers. If you press ctrl+C it will stop the rostopic echo process and it will be easier to see the data. The most important informations you should see are:

- angle_min
- angle_max
- time_increment
- angle_increment
- scan_time
- range_min
- range_max
- ranges

The most important one is ranges. it is a list of data which correspond to the coordinates the detected objects. To see just this list you can have the command:

```
rostopic echo /scan/ranges
```

### Setting SLAM using ROS

To manage to use SLAM with the Rplidar we will use a project already made by hector_slam, all credits goes to him: https://github.com/tu-darmstadt-ros-pkg/hector_slam

You need to go on your /src folder of your workspace and git clone the project

```
git clone https://github.com/tu-darmstadt-ros-pkg/hector_slam.git
```

 We will have to modify some launchers of the hector_slam package to run it with our RPlidar. SLAM is working with predefined topics and referentials we common have on a robot and in our case we will have to modify them because it is not the case for us. 
 
 > First go on the folder hector_slam/hector_mapping/launch/mapping_default.launch
 
 In this launchfile, SLAM is working as if the base frame was the base_footprint topics but it is not the case for us, it is the base_link. Also the same for the odom_frame. So we have to change three lines (the 5th, the 6th and the 57th lines).  
 
```
  <arg name="base_frame" default="laser"/>
  <arg name="odom_frame" default="laser"/>
  <node pkg="tf" type="static_transform_publisher" name="base_to_laser_broadcaster" args="0 0 0 0 0 0 map nav 100"/>
```

> Then we need to go on a second launchfile hector_slam/hector_slam_launch/launch/tutorial.launch
> In this launchfile you just have to change the use_sim_time into false. It means we are not in simulation anymore but in real life. 

```
<param name="/use_sim_time" value="false"/>
```

### Run SLAM with the RPlidar 

On one terminal launch this launchfile with this command (don't forget to source devel/setup.bash)
```
roslaunch rplidar_ros rplidar.launch
```

On a second terminal launch this launchfile with this command (don't forget to source devel/setup.bash)
```
roslaunch hector_slam_launch tutorial.launch
```

You should have your RPlidar working and the mapping being done on Rviz. 

# ---------------------------------------------------------------------------------------

# Tuto: How to implement a MPU9250 on RaspberryPi 3B+ with python

This tutorial is going to show you how to implement a MPU9250 on a RaspberryPi 3B+ and get the Pitch/Yaw/Roll. The MPU9250 is the same as a MPU6050 but has a gyroscope, accelerometer and magnetometer contrary to the MPU6050 which just have gyroscope and accelerometer. We will use a code working for a MPU6050 but it iss working for the MPU9250 as well (we just won't use the magnetometer)

##### Robot Project - CPE Lyon 2020 / 2021
###
### Created by Nicolas Guy on Fri 15/01/2021

Setting used:
  - Ubuntu 18.04
  - ROS Kinetic
  - Catkin
  - RaspberryPi 3B+

### How to plug the MPU9250 to the RaspberryPi 3B+

  You will need four jumpers to connect the MPU9250 to the RaspberryPi. 
  
  > The MPU9250 needs 3.3V (watch out not to connect it to 5V). The communication between the MPU9250 and the RaspberryPi is a I²C communication. One pin is for the Clock (SDL) and another one is for the datas (SDA)

  - VCC -> Pin 1
  - GND -> Pin 6
  - SDA -> Pin 3
  - SCL -> Pin 5 

### Enable the I²C communication on the RaspberryPi

If you haven't already worked with I²C before on your RaspberryPi you will have to enable to I²C communication. To do that you first need to follow the next steps:

Open a terminal and write this command
```
sudo raspi-config
```
This will launch the raspi-config utility. Select "Interfacing Options".

Then select "I2C" and "Yes".

You can now select "Finish". You will need to reboot your RaspberryPi and then, the I²C communication would be enabled on your RapsberryPi.

### Test the MPU9250 on your RaspberryPi 3B+

You will need to add a library on your RaspberryPi. To do that use the command: 

```

```

You are now ready to make your first test with the MPU9250 connected to your RaspberryPI using the I2C communication. 

To do that, big respect to Geir Istad and his github exemple he made. He said that everybody can use his code and the filter he made to get the Pitch/Yaw/ROll with an amazing precision and without a magnetometer (which is super impresive).

You can find the project at this link: https://github.com/thisisG/MPU6050-I2C-Python-Class

Open a terminal and do this command:

```
git clone https://github.com/thisisG/MPU6050-I2C-Python-Class.git
```

You will probably need to make all the python scripts executable (chmod +x). 

Finally, on my MPU9250 I needed to change a bit the parameters of the algorithm. To do that I opened the MPU6050_example.py script and modified the line 79 like this:

```
print('yaw: ' + str(roll_pitch_yaw.z*2))
```

Then save and you can run the example code on a terminal

```
python MPU6050_example.py 
```

You should see the Pitch/Yaw/Roll on your terminal and the modification when you move the MPU9250. The MPU accumulate an error with the time so if you want something more precise without any error you can add a PID or a Kalman filter for example. 



### More Informations:

| Website | Link |
| ------ | ------ |
| RPLidar/RaspberryPu | https://medium.com/robotics-with-ros/installing-the-rplidar-lidar-sensor-on-the-raspberry-pi-32047cde9588|
| Youtube Video to implement an RPLidar | https://www.youtube.com/watch?v=Qrtz0a7HaQ4 |
| Youtube video to see an exemple of Lidar with SLAM | https://www.youtube.com/watch?v=qNdcXUEF7KU&ab_channel=RoboticsWeekends|
| Github project RPi - IMU | https://github.com/pcdangio/ros-driver_mpu9250 |
# ---------------------------------------------------------------------------------------------

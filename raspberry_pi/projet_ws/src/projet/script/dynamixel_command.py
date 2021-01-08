#!/usr/bin/env python

import rospy
import sys
from std_msgs.msg import Float64, Bool


class dynamixel_command:
    POSITION_OPEN = 0
    POSITION_CLOSE = 4@

    def __init__(self):
        rospy.init_node('Dynamixel_command', anonymous=True)
        #Publishers   
        self.pub_position = rospy.Publisher("/tilt_controller/command", Float64, queue_size = 10)
        rospy.sleep(1)
        rospy.loginfo("[dynamixel_command] node started")
        #Subscribers
        rospy.Subscriber("/balayage", Bool, self.set_position)

        rospy.spin()

       
    def set_position(self,data):
        """
        when receive the topic [/balayage] set the position of the dynamixel depending of the capteur value (TRUE or FALSE)
        """
        #rostopic pub -1 /dual_motor_controller/command std_msgs/Float64 -- 1.5
        capteur = data.data
        try:
            if capteur == True:
                position = self.POSITION_OPEN     
                rospy.loginfo("Position min")           

            elif capteur == False:
                position = self.POSITION_CLOSE
                rospy.loginfo("Position max")
            self.pub_position.publish(position)
            
        except rospy.ServiceException as e:
            rospy.logwarn("Service call failed: %s"%e)

        

if __name__ == '__main__':

    try:
        command = dynamixel_command()
        
        #command.set_position(position)

    except rospy.ROSInterruptException:
        pass

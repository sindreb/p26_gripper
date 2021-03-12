#!/usr/bin/env python

import sys
import copy
import rospy
import geometry_msgs.msg
from std_msgs.msg import String, Int64, Float32

cylinder_com = geometry_msgs.msg.Point()

def callback_com(data):
    global cylinder_com
    cylinder_com = data
    rospy.loginfo("Received cylinder center of mass: %f , %f , %f", cylinder_com.x, cylinder_com.y, cylinder_com.z)

def main():

        rospy.init_node('raspberry_com', anonymous=True)

        rospy.Subscriber("p26_lefty/cylinder_com", geometry_msgs.msg.Point, callback_com)
        str = "Waiting for cylinder com..."
        rospy.loginfo(str)

        rospy.wait_for_message("p26_lefty/cylinder_com", geometry_msgs.msg.Point, timeout=None)
        rate = rospy.Rate(10)


main()

#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Int64, Float32

def grip_procedure(data):
    global actuation
    actuation = data


def open_grip():
    #Opening gripper
    gripper_pos = 'open'
    rospy.loginfo("Gripper open")
    pub.publish(gripper_pos)
    rate.sleep()

def close_grip():
    #Closing gripper
    gripper_pos = 'closed'
    rospy.loginfo("Gripper closed")
    pub.publish(gripper_pos)
    rate.sleep()


def main():

    pub = rospy.Publisher('p26_lefty/gripper', Int64, queue_size=10)
    rospy.init_node('gripper', anonymous=True)
    rate = rospy.Rate(10)
    rospy.Subscriber("p26_lefty/gripper", Int64, grip_procedure)
    rospy.loginfo("Gripper initialized, ready for input")
    rospy.wait_for_message("p26_lefty/gripper", Int64, timeout=None)

    if actuation == 1:
        rospy.loginfo("Opening gripper...")
        open_grip()

    elif actuation == 2:
        rospy.loginfo("Closing gripper...")
        close_grip()

while True:
    main()

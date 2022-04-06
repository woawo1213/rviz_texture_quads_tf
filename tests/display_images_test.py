#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose

import copy
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
import rospkg
import tf
import math

from rviz_textured_quads.msg import TexturedQuad, TexturedQuadArray


def pub_image():

    rospy.init_node('rviz_display_image_test', anonymous=True)
    rospack = rospkg.RosPack()

    image_pub = rospy.Publisher("/semantic_targets", TexturedQuadArray, queue_size=10)

    texture_path = rospack.get_path('rviz_textured_quads') + '/tests/textures/'
    img1 = cv2.imread(texture_path + 'red.jpg',cv2.IMREAD_COLOR)
    img_msg1 = CvBridge().cv2_to_imgmsg(img1, "bgr8")

    display_image = TexturedQuad()
    
    pose = Pose()
    
    pose.position.x =  -1.2
    pose.position.y =  -0.5
    pose.position.z =  2.0

    pose.orientation.x = 0.0
    pose.orientation.y = 0.0
    pose.orientation.z = 0.0
    pose.orientation.w = 1.0

    scale = 0.5

    display_image.image = img_msg1
    display_image.pose = pose
    display_image.width = scale 
    display_image.height = (scale * img_msg1.height)/img_msg1.width
    display_image.border_color = [1., 0., 0., 0.5]
    display_image.border_size = 0.05
    display_image.caption = 'Marker'
    display_image.image.header.frame_id = 'map'


    display_images = TexturedQuadArray()
    display_images = np.array([display_image])

    rate = rospy.Rate(1) # 1Hz
    count = 0

    while not rospy.is_shutdown():
        if False:  # (cap.isOpened()):
            ret, frame = cap.read()

            display_image.image = CvBridge().cv2_to_imgmsg(frame, "bgr8")

        image_pub.publish(display_images)
        rate.sleep()

    # cap.release()

if __name__ == '__main__':

    try:
        pub_image()
    except rospy.ROSInterruptException:
        pass

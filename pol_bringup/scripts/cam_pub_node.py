#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage

import numpy as np
import cv2

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('cam_pub_node')
        # Create a publishers
        self.pub_img = self.create_publisher(CompressedImage, 'camera/image_raw', 10)
        
        # Create a timer to publish frames at 60 Hz
        self.timer = self.create_timer(1/60.0, self.publish_image)
        
        # Params
        self.width = 1920
        self.height = 1080
        self.channels = 3
        
        # Color pointer
        self.i = 0
        self.i_red = 255
        self.i_green = 511
        self.i_blue = 767
        

    def publish_image(self):
        # Dummy image
        image_np = np.zeros(shape=(self.height, self.width, self.channels), dtype=np.uint8)
        
        pixel_rgb = [
            self.i       if  (0            <=  self.i  <= self.i_red  )  else 255,
            self.i - 256 if  (self.i_red   <   self.i  <= self.i_green)  else 255,
            self.i - 512 if  (self.i_green <   self.i  <= self.i_blue )  else 255,
        ]
        
        image_np[:, :] = pixel_rgb
        
        msg = CompressedImage()
        msg.header.stamp = self.get_clock().now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', image_np)[1]).tostring()
        # Publish image
        self.image_pub.publish(msg)
        
        self.i += 1
        if self.i == self.i_blue:
            self.i = 0

    def destroy_node(self):
        # Release the camera when shutting down
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()


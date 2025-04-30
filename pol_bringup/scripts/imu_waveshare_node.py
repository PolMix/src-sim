#!/usr/bin/python3

# Python imports
import time
import threading

# Basic imports
import rclpy
from rclpy.node import Node

# ROS msgs import
from sensor_msgs.msg import Imu, MagneticField


class ImuWaveshare(Node):
    def __init__(self):
        super().__init__('imu_waveshare_node')
        
        self.__bus_state = 0

        self.time_now = self.get_clock().now().to_msg()
        
        #---------- IMU measurement storage ----------
        self.val = {
            'a': [0.0, 0.0, 0.0],
            'g': [0.0, 0.0, 0.0],
            'm': [0.0, 0.0, 0.0],
            'q': [1.0, 0.0, 0.0, 0.0],
        }
        

        #---------- ROS publishers ----------
        self.pub_imu = self.create_publisher(Imu, 'imu/data', 10)
        self.pub_mag = self.create_publisher(MagneticField, 'imu/mag', 10)
        
        self.publishing_active = True
        self.timer = self.create_timer(1/100.0, self.publish_data)  # publish frames at 100 Hz
        
        
        #---------- Fill constant values to ROS msgs ----------
        # Insert constant fields of the Imu msg
        self.msg_imu = Imu()
        self.msg_imu.header.frame_id = "base_link"
        
        self.msg_imu.orientation_covariance = [0.05, 0.0, 0.0, 
           0.0, 0.05, 0.0 ,
           0.0, 0.0 , 0.05]
        self.msg_imu.angular_velocity_covariance = [0.05, 0.0, 0.0, 
            0.0, 0.05, 0.0 ,
            0.0, 0.0 , 0.05]
        self.msg_imu.linear_acceleration_covariance = [0.05, 0.0, 0.0, 
            0.0, 0.05, 0.0 ,
            0.0, 0.0 , 0.05]
        
        # Insert constant fields of the Mag msg
        self.msg_mag = MagneticField()
        self.msg_mag.header.frame_id = "base_link"
        
        self.msg_mag.magnetic_field_covariance = [0.05, 0.0, 0.0, 
            0.0, 0.05, 0.0 ,
            0.0, 0.0 , 0.05]



    def start_receive_threading(self):
        try:
            if self.__bus_state == 0:
                thread_name = "task_imu_receive"
                task_receive = threading.Thread(target=self.receive_data, name=thread_name)
                task_receive.daemon = True
                task_receive.start()
                self.get_logger().info("\x1B[32mIMU receive threading has started\033[0m\t\t")
                self.__bus_state = 1
                time.sleep(0.25)
        except:
            self.get_logger().info("\x1B[31mIMU receive threading has failed\033[0m\t\t")
            pass


    
    def receive_data(self):

        self.time_now = self.get_clock().now().to_msg()
        dummy_values = [i / 10.0 for i in range(0, 100)]
        i = 0
        while True:
            time.sleep(0.05)
            self.val['a'][0] = float(dummy_values)
            self.val['a'][1] = float(dummy_values)
            self.val['a'][2] = float(dummy_values)
            
            self.val['g'][0] = float(dummy_values)
            self.val['g'][1] = float(dummy_values)
            self.val['g'][2] = float(dummy_values)
            
            self.val['q'][0] = float(dummy_values)
            self.val['q'][1] = float(dummy_values)
            self.val['q'][2] = float(dummy_values)
            self.val['q'][3] = float(dummy_values)
            
            self.val['m'][0] = float(dummy_values)
            self.val['m'][1] = float(dummy_values)
            self.val['m'][2] = float(dummy_values)
            
            i += 1
            
            if i == 100:
                i = 0
    
    
    def publish_data(self):
        
        # Check if publishing hasn't been allowed yet
        if not self.publishing_active:
            return
        
        # Acc and Gyr
        self.msg_imu.header.stamp = self.time_now
        
        self.msg_imu.orientation.x = self.val['q'][1]
        self.msg_imu.orientation.y = self.val['q'][2]
        self.msg_imu.orientation.z = self.val['q'][3]
        self.msg_imu.orientation.w = self.val['q'][0]
        
        self.msg_imu.linear_acceleration.x = self.val['a'][0]
        self.msg_imu.linear_acceleration.y = self.val['a'][1]
        self.msg_imu.linear_acceleration.z = self.val['a'][2]
        
        self.msg_imu.angular_velocity.x = self.val['g'][0]
        self.msg_imu.angular_velocity.y = self.val['g'][1]
        self.msg_imu.angular_velocity.z = self.val['g'][2]
    
        self.pub_imu.publish(self.msg_imu)
        
        # Mag
        self.msg_mag.header.stamp = self.time_now
        self.msg_mag.magnetic_field.x = self.val['m'][0]
        self.msg_mag.magnetic_field.y = self.val['m'][1]
        self.msg_mag.magnetic_field.z = self.val['m'][2]
        
        self.pub_mag.publish(self.msg_mag)
        

    def destroy_node(self):
        super().destroy_node()
        
        
        
def main(args=None):
    # Init ROS2 routines
    rclpy.init(args=args)
    
    # Init node
    node = ImuWaveshare()
    node_name = "ImuWaveshare"
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info(f"{node_name} shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

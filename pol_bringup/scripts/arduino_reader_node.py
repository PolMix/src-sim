#!/usr/bin/python3

# Python imports
import threading
import time

# Basic imports
import rclpy
from rclpy.node import Node

# ROS msgs import
from sensor_msgs.msg import Range
from pol_msgs.msg import BinaryDetectionStamped

class ArduinoReader(Node):
    def __init__(self):
        super().__init__('arduino_reader_node')
        #---------- Param assignment ----------
        self.__uart_state = 0
        
        
        #---------- Storage for measurements ----------
        self.val = {'SND1': 0,
                    'IROB': 0,
                    'IRM1': 0,
                    'TLT1': 0}
        
        
        #---------- Create publishers ----------
        self.pub_sound = self.create_publisher(Range, 'sound_radar/range', 10)
        self.pub_ir_obst = self.create_publisher(BinaryDetectionStamped, 'ir_obstacle/detection', 10)
        self.pub_ir_motion = self.create_publisher(BinaryDetectionStamped, 'ir_motion/detection', 10)
        self.pub_tilt = self.create_publisher(BinaryDetectionStamped, 'tilt/detection', 10)
        
        # Create a timer to publish frames at 5 Hz
        self.timer = self.create_timer(1/5.0, self.publish_data)
        
        # Insert constant fields of the sound radar msg
        self.msg_sound = Range()
        self.msg_sound.header.frame_id = "sound_link"
        self.msg_sound.radiation_type = 0  # useless
        self.msg_sound.field_of_view = 15.0  # degrees
        self.msg_sound.min_range = 1.0  # cm
        self.msg_sound.max_range = 800.0  # cm
        
        # Insert constant fields of the ir obstacle detector msg
        self.msg_ir_obst = BinaryDetectionStamped()
        self.msg_ir_obst.header.frame_id = "ir_obstacle_link"
        
        # Insert constant fields of the ir obstacle detector msg
        self.msg_ir_motion = BinaryDetectionStamped()
        self.msg_ir_motion.header.frame_id = "ir_motion_link"
        
        # Insert constant fields of the ir obstacle detector msg
        self.msg_tilt = BinaryDetectionStamped()
        self.msg_tilt.header.frame_id = "tilt_link"
        
    def start_receive_threading(self):
        try:
            if self.__uart_state == 0:
                thread_name = "task_serial_receive"
                task_receive = threading.Thread(target=self.receive_data, name=thread_name)
                task_receive.setDaemon(True)
                task_receive.start()
                self.get_logger().info("\x1B[32mArduinoReader threading has successfully started!\033[0m\t\t")
                self.__uart_state = 1
                time.sleep(0.25)
        except:
            self.get_logger().info("\x1B[31mArduinoReader threading has failed!\033[0m\t\t")
            pass
    
    def receive_data(self):
        
        i = 0
        while True:
            time.sleep(0.05)
            
            if i == 0:
                self.val['SND1'] = 1
            elif i == 1:
                self.val['IROB'] = 1
            elif i == 2:
                self.val['IRM1'] = 1
            elif i == 3:
                self.val['TLT1'] = 1
            
            i += 1
            
            if i == 3:
                i = 0
            

    def publish_data(self):
        time_now = self.get_clock().now().to_msg()
        
        # Sound range
        self.msg_sound.header.stamp = time_now
        self.msg_sound.range = float(self.val['SND1'])
        self.pub_sound.publish(self.msg_sound)
        
        # IR obstacle
        self.msg_ir_obst.data = int(self.val['IROB'])
        self.msg_ir_obst.header.stamp = time_now
        self.pub_ir_obst.publish(self.msg_ir_obst)
        
        # IR motion
        self.msg_ir_motion.data = int(self.val['IRM1'])
        self.msg_ir_motion.header.stamp = time_now
        self.pub_ir_motion.publish(self.msg_ir_motion)
        
        # Tilt
        self.msg_tilt.data = int(self.val['TLT1'])
        self.msg_tilt.header.stamp = time_now
        self.pub_tilt.publish(self.msg_tilt)
        
        

    def destroy_node(self):
        # Release the camera when shutting down
        super().destroy_node()

def main(args=None):
    # Init ROS2 routines
    rclpy.init(args=args)
    
    # Init node
    node = ArduinoReader()
    node_name = "ArduinoReader"
    node.start_receive_threading()
    
    # Wait some time before receiving data
    time.sleep(0.25)
    
    #
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info(f"{node_name} shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()


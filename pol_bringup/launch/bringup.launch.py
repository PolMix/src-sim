from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
  
  
  return LaunchDescription([
    
    # IMU reader node
    Node(
      package    = 'pol_bringup'          ,
      executable = 'imu_waveshare_node.py',
      name       = 'imu_waveshare_node'   ,
      output     = 'screen'               ,
    ),
    
    Node(
      package    = 'pol_bringup'           ,
      executable = 'arduino_reader_node.py',
      name       = 'arduino_reader_node'   ,
      output     = 'screen'                ,
    ),
    
    Node(
      package    = 'pol_bringup'    ,
      executable = 'cam_pub_node.py',
      name       = 'cam_pub_node'   ,
      output     = 'screen'         ,
    ),
    
  ])







# MISC
"""
# Madgwick filter
node_madgwick_filter = Node(
  package    = 'imu_filter_madgwick'     ,
  executable = 'imu_filter_madgwick_node',
  name       = 'madgwick_filter'         ,
  output     = 'screen'                  ,
  parameters = [param_file_madgwick]  ,
  remappings = [
    ('/imu/data_raw' , '/imu/data_raw'),
    ('/imu/data'     , '/imu/data'    ),
    ('/imu/mag'      , '/imu/mag_raw' ),],
)
  
  
  
  
# Hiwonder IMU node
node_imu_hiwonder = Node(
  package    = 'wit_ros2_imu',
  executable = 'wit_ros2_imu',
  name       = 'imu_hiwonder_node',
  parameters = [
    {'port': '/dev/ttyUSB0'},
    {"baud": 9600          }
  ],
  remappings = [
    ('/imu/data_raw', '/imu_hw/data')
  ],
  output     = "screen"
)
  
# GPS decoder node
node_navsat_driver = Node(
  package    = 'nmea_navsat_driver',
  executable = 'nmea_serial_driver',
  name       = 'nmea_driver_node'  ,
  parameters = [{
    'port'     : '/dev/ttyAMA1',
    'baud'     : 9600          ,
    'frame_id' : 'base_link'   }
  ],
  output     = "screen",
)




# Usb-cam node
usb_cam_node = Node(
  package    = 'usb_cam',
  executable = 'usb_cam_node_exe',
  name       = 'usb_cam',
  output     = 'screen',
  parameters = [{
    'video_device' : '/dev/video0',
    'frame_id'     : 'camera_frame',
    'io_method'    : 'mmap',
    'pixel_format' : 'yuyv',
    'image_width'  : 1920,
    'image_height' : 1080,
    'framerate'    : 40.0}
  ]
),




# Flashligh decoder node
node_flashlight_decoder= Node(
  package    = 'pol_nav'                       ,
  executable = 'flashlight_decoder_node_new.py',
  name       = 'flashlight_decoder_node_new'   ,
  output     = 'screen'                        ,
  parameters = [{
    'brightness_thr' : 200 ,  # threshold for flashlight's brightness, [0, 255]
    'baseline_len'   : 0.2 ,  # distance between cameras (in meters)
    'focal_len'      : 2950,  # focal len in px = img_width_px * focal_len_mm / CCD_size_mm
    'time_window'    : 10  ,
  }],
  remappings = [
    ('/camera/left/ptr', '/camera/left/ptr')
  ]
)




# Package to republish images from shared memory pointers
gal_cam_pub_left = Node(
      package    = 'pol_bringup'         ,
      namespace  = 'camera'              ,
      executable = 'camera_frame_node.py',
      parameters = [{
        'new_w'        : 720         ,
        'new_h'        : 480          ,
        'role'         : 'master'     ,
      }],
      remappings = [
        ('/ptr'          , '/camera/left/ptr_1'        ),
        ('/image_resized', '/camera/left/image_resized'),
      ]
    ),
    
    gal_cam_pub_right = Node(
      package    = 'pol_bringup'         ,
      namespace  = 'camera'              ,
      executable = 'camera_frame_node.py',
      parameters = [{
        'new_w'        : 1280         ,
        'new_h'        : 720          ,
        'role'         : 'slave'      ,
      }],
      remappings = [
        ('/ptr'          , '/camera/right/ptr_1'        ),
        ('/image_resized', '/camera/right/image_resized'),
        ('/image'        , '/camera/right/image'        )
      ]
    ),
"""


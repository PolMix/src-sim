cmake_minimum_required(VERSION 3.8)
project(pol_bringup)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()


#---------- Basic ----------
# Find dependencies
find_package(ament_cmake        REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp             REQUIRED)
find_package(rclpy              REQUIRED)

find_package(std_msgs            REQUIRED)
find_package(sensor_msgs         REQUIRED)
find_package(geometry_msgs       REQUIRED)
find_package(nav_msgs            REQUIRED)
find_package(pol_msgs            REQUIRED)


#---------- Directories, launch and parameter files ----------
# include dir
install(
  DIRECTORY include/
  DESTINATION include
)

#---- Launch files ----
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

#---- Parameter files ----
install(
  DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)



#----------------------------
#---------- Python ----------
#----------------------------
# Install Python modules
ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(PROGRAMS
  scripts/arduino_reader_node.py
  scripts/cam_pub_node.py
  scripts/imu_waveshare_node.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install folders with other python scripts and files
install(
  DIRECTORY pol_bringup/
  DESTINATION lib/${PROJECT_NAME}
  USE_SOURCE_PERMISSIONS
)


#---------- Testing ----------
# Automates the process of setting up linting for the package, which
# is the process of running tools that analyze the code for potential
# errors, style issues, and other discrepancies that do not adhere to
# specified coding standards or best practices.
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  
  # The following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  
  # The following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()
 
# Used to export include directories of a package so that they can be easily
# included by other packages that depend on this package.
ament_export_include_directories(include)

# Export libs
ament_export_libraries(${GX_LIB})
 
# Generate and install all the necessary CMake and environment hooks that 
# allow other packages to find and use this package.
ament_package()

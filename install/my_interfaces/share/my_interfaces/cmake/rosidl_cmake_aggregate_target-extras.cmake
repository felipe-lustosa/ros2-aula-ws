# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target my_interfaces::my_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${my_interfaces_TARGETS}.
if(my_interfaces_TARGETS AND NOT TARGET my_interfaces::my_interfaces)
  add_library(my_interfaces::my_interfaces INTERFACE IMPORTED)
  set_target_properties(my_interfaces::my_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${my_interfaces_TARGETS}")
endif()

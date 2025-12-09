cmake_minimum_required(VERSION 3.15)
project(TrajectoryGenerator)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Options
option(USE_CUDA "Enable CUDA support" OFF)

# Find ONNX Runtime
# You may need to set ONNXRUNTIME_ROOT_DIR to point to your ONNX Runtime installation
# Example: cmake -DONNXRUNTIME_ROOT_DIR=/path/to/onnxruntime ..

if(DEFINED ENV{ONNXRUNTIME_ROOT_DIR})
    set(ONNXRUNTIME_ROOT_DIR $ENV{ONNXRUNTIME_ROOT_DIR})
endif()

if(ONNXRUNTIME_ROOT_DIR)
    message(STATUS "Using ONNX Runtime from: ${ONNXRUNTIME_ROOT_DIR}")
    
    set(ONNXRUNTIME_INCLUDE_DIRS ${ONNXRUNTIME_ROOT_DIR}/include)
    
    if(WIN32)
        set(ONNXRUNTIME_LIBRARIES ${ONNXRUNTIME_ROOT_DIR}/lib/onnxruntime.lib)
    elseif(APPLE)
        set(ONNXRUNTIME_LIBRARIES ${ONNXRUNTIME_ROOT_DIR}/lib/libonnxruntime.dylib)
    else()
        set(ONNXRUNTIME_LIBRARIES ${ONNXRUNTIME_ROOT_DIR}/lib/libonnxruntime.so)
    endif()
else()
    # Try to find system-installed ONNX Runtime
    find_path(ONNXRUNTIME_INCLUDE_DIRS
        NAMES onnxruntime_cxx_api.h
        PATHS /usr/include /usr/local/include
        PATH_SUFFIXES onnxruntime onnxruntime/core/session
    )
    
    find_library(ONNXRUNTIME_LIBRARIES
        NAMES onnxruntime
        PATHS /usr/lib /usr/local/lib
    )
endif()

if(NOT ONNXRUNTIME_INCLUDE_DIRS OR NOT ONNXRUNTIME_LIBRARIES)
    message(FATAL_ERROR 
        "ONNX Runtime not found! Please set ONNXRUNTIME_ROOT_DIR or install ONNX Runtime.\n"
        "Download from: https://github.com/microsoft/onnxruntime/releases\n"
        "Then set: export ONNXRUNTIME_ROOT_DIR=/path/to/onnxruntime"
    )
endif()

message(STATUS "ONNX Runtime include: ${ONNXRUNTIME_INCLUDE_DIRS}")
message(STATUS "ONNX Runtime library: ${ONNXRUNTIME_LIBRARIES}")

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${ONNXRUNTIME_INCLUDE_DIRS}
)

# Library
add_library(trajectory_inference
    trajectory_inference.cpp
)

target_link_libraries(trajectory_inference
    ${ONNXRUNTIME_LIBRARIES}
)

# Executable
add_executable(trajectory_demo
    main.cpp
)

target_link_libraries(trajectory_demo
    trajectory_inference
    ${ONNXRUNTIME_LIBRARIES}
)

# Installation
install(TARGETS trajectory_demo trajectory_inference
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

install(FILES trajectory_inference.h
    DESTINATION include
)

# Print build information
message(STATUS "")
message(STATUS "========================================")
message(STATUS "Trajectory Generator Configuration")
message(STATUS "========================================")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "CUDA Support: ${USE_CUDA}")
message(STATUS "========================================")

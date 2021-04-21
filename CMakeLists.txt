cmake_minimum_required(VERSION 2.8)

project(test)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -g -O0 -Wno-deprecated")

set(ROOT_DIR ${PROJECT_SOURCE_DIR})

aux_source_directory(${ROOT_DIR}/src varsrc)

include_directories(${ROOT_DIR}/src)

add_executable(test ${varsrc})

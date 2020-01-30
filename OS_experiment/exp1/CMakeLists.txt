cmake_minimum_required(VERSION 3.14)
project(lab C)

set(CMAKE_C_STANDARD 99)

add_executable(lab main.c)

find_package(Threads REQUIRED)
target_link_libraries(lab Threads::Threads)
# CMake manifest file for compiling C++ code.
#
# For more information, visit https://cmake.org/cmake/help/latest/.

cmake_minimum_required(VERSION 3.15...4.1)
project(
  {{ cookiecutter.__project_package }}
  DESCRIPTION "{{ cookiecutter.project_description }}"
  LANGUAGES CXX
  VERSION 0.1.0
)

option(BUILD_TEST "Build test suite" OFF)

# For editor integration.
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(BUILD_TEST)
  find_package(Catch2 REQUIRED)

  add_executable(test src/lib.cpp)
  target_compile_definitions(test PRIVATE TEST)
  target_link_libraries(test PRIVATE Catch2::Catch2WithMain)
else()
  find_package(argparse REQUIRED)

  add_library(lib STATIC src/lib.hpp src/lib.cpp)
  add_executable({{ cookiecutter.__project_package }} src/main.cpp)
  target_link_libraries({{ cookiecutter.__project_package }} argparse::argparse lib)
endif()

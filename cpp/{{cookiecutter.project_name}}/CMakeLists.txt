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

file(
  GLOB_RECURSE
  lib_sources
  RELATIVE
  ${CMAKE_CURRENT_SOURCE_DIR}
  CONFIGURE_DEPENDS
  src/*.cpp
)
list(REMOVE_ITEM lib_sources src/main.cpp)

if(BUILD_TEST)
  find_package(Catch2 REQUIRED)

  file(
    GLOB_RECURSE
    test_sources
    CONFIGURE_DEPENDS
    test/*.cpp
  )
  add_executable(test ${lib_sources} ${test_sources})
  target_compile_definitions(test PRIVATE TEST)
  target_link_libraries(test Catch2::Catch2WithMain)
else()
  find_package(argparse REQUIRED)

  add_library(lib STATIC ${lib_sources})
  add_executable({{ cookiecutter.__project_package }} src/main.cpp)
  target_link_libraries({{ cookiecutter.__project_package }} argparse::argparse lib)
endif()

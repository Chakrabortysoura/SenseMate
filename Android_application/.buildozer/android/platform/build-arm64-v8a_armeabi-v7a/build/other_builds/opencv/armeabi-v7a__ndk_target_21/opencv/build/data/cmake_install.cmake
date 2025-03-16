# Install script for directory: /home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/build/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "TRUE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/home/souranil/.buildozer/android/platform/android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xlibsx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/etc/haarcascades" TYPE FILE FILES
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_eye.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_frontalcatface.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_frontalcatface_extended.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_frontalface_alt.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_frontalface_alt2.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_frontalface_alt_tree.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_fullbody.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_lefteye_2splits.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_licence_plate_rus_16stages.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_lowerbody.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_profileface.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_righteye_2splits.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_russian_plate_number.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_smile.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/haarcascades/haarcascade_upperbody.xml"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xlibsx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/etc/lbpcascades" TYPE FILE FILES
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/lbpcascades/lbpcascade_frontalcatface.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/lbpcascades/lbpcascade_frontalface.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/lbpcascades/lbpcascade_frontalface_improved.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/lbpcascades/lbpcascade_profileface.xml"
    "/home/souranil/Source-Code/Final_Year_Project/Codebase/Android_application/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/data/lbpcascades/lbpcascade_silverware.xml"
    )
endif()


#! /usr/bin/bash

echo "Start of git pull request"
git pull origin main
echo "Pull ended "
echo "Start of the build script\n"  
cd Android_application
source project/bin/activate
buildozer -v android debug
deactivate
echo "Build process ended"
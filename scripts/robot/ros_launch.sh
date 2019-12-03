#!/usr/bin/env bash


ROS_APP_PATH=$1
ROS_APP_NAME=$2
ROS_ENTRY_POINT=$3
shift
shift
shift

ROSDISTRO="dashing"
ROS2="/opt/ros/dashing/setup.bash"
CYCLONE="/home/ubuntu/workspace/ros2_ws/install/setup.bash"

USER="ubuntu"

WD=$(pwd)
echo $WD
trap cleanup 1 2 3 6

cleanup(){

    screen -S rosapp -X quit
    exit 0
}


# Kill previous sessions
echo "==== Killing ROS2 old screen sessions"
screen -S rosapp -X quit
sleep 1

echo "=== Build ROS2 Application"
source $ROS2
source $CYCLONE

cd $ROS_APP_PATH

sudo rosdep install -i --from-path . --rosdistro $ROSDISTRO -y
colcon build --packages-select $ROS_APP_NAME

cd $WD
# ros
echo "==== Starting ROS2 Application"
CMD="$PWD/app.sh $ROS_APP_PATH $ROS_APP_NAME $ROS_ENTRY_POINT $@"
#echo $CMD
screen -S rosapp -dm $CMD
sleep 1

screen -ls

while :
do
    sleep 1
done
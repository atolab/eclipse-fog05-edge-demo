#!/bin/bash -e

ROS_APP_PATH=$1
ROS_APP_NAME=$2
ROS_ENTRY_POINT=$3

shift
shift
shift


ROSDISTRO="dashing"
ROS2="/opt/ros/dashing/setup.bash"
CYCLONE="/home/ubuntu/workspace/ros2_ws/install/setup.bash"

cd $ROS_APP_PATH
source $ROS2
source $CYCLONE
. install/setup.bash
while [ True ];
do
	ros2 run $ROS_APP_NAME $ROS_ENTRY_POINT $@
	sleep 1
done
import os
import sys

from launch import LaunchDescription
from launch.actions import OpaqueFunction
from moveit_configs_utils.launches import generate_moveit_rviz_launch

sys.path.append(os.path.dirname(__file__))
from camera_moveit_config_utils import build_cr5_moveit_config


def generate_launch_description():
    def _launch_setup(context, *args, **kwargs):
        moveit_config = build_cr5_moveit_config(context)
        return [generate_moveit_rviz_launch(moveit_config)]

    return LaunchDescription([OpaqueFunction(function=_launch_setup)])

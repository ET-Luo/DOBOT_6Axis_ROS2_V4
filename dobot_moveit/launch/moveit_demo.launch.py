from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory
def generate_launch_description():
    name = os.getenv("DOBOT_TYPE")
    package_name = f'{name}_moveit'
    urdf_name = "demo.launch.py"

    pkg_share = os.path.join(get_package_share_directory(package_name))

    moveit_model_path = os.path.join(pkg_share,'launch',urdf_name)
    ld = LaunchDescription()
    use_ee_camera_arg = DeclareLaunchArgument(
        'use_ee_camera',
        default_value='true',
        description='Enable end-effector camera link in robot description (CR5 only).'
    )
    camera_profile_arg = DeclareLaunchArgument(
        'camera_profile',
        default_value='short',
        description='Camera profile preset: short or long (CR5 only).'
    )
    camera_length_arg = DeclareLaunchArgument(
        'camera_length',
        default_value='-1',
        description='Override camera length in meters; <= 0 uses profile default (CR5 only).'
    )
    camera_width_arg = DeclareLaunchArgument(
        'camera_width',
        default_value='-1',
        description='Override camera width in meters; <= 0 uses profile default (CR5 only).'
    )
    camera_height_arg = DeclareLaunchArgument(
        'camera_height',
        default_value='-1',
        description='Override camera height in meters; <= 0 uses profile default (CR5 only).'
    )
    camera_offset_x_arg = DeclareLaunchArgument(
        'camera_offset_x',
        default_value='0.03',
        description='Camera offset X from Link6 in meters (CR5 only).'
    )
    camera_offset_y_arg = DeclareLaunchArgument(
        'camera_offset_y',
        default_value='0.0',
        description='Camera offset Y from Link6 in meters (CR5 only).'
    )
    camera_offset_z_arg = DeclareLaunchArgument(
        'camera_offset_z',
        default_value='0.06',
        description='Camera offset Z from Link6 in meters (CR5 only).'
    )
    ld.add_action(use_ee_camera_arg)
    ld.add_action(camera_profile_arg)
    ld.add_action(camera_length_arg)
    ld.add_action(camera_width_arg)
    ld.add_action(camera_height_arg)
    ld.add_action(camera_offset_x_arg)
    ld.add_action(camera_offset_y_arg)
    ld.add_action(camera_offset_z_arg)

    include_kwargs = {}
    if name == 'cr5':
        include_kwargs['launch_arguments'] = {
            'use_ee_camera': LaunchConfiguration('use_ee_camera'),
            'camera_profile': LaunchConfiguration('camera_profile'),
            'camera_length': LaunchConfiguration('camera_length'),
            'camera_width': LaunchConfiguration('camera_width'),
            'camera_height': LaunchConfiguration('camera_height'),
            'camera_offset_x': LaunchConfiguration('camera_offset_x'),
            'camera_offset_y': LaunchConfiguration('camera_offset_y'),
            'camera_offset_z': LaunchConfiguration('camera_offset_z')
        }.items()

    included_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(moveit_model_path),
        **include_kwargs
    )
    ld.add_action(included_launch)

    # 添加其他操作...
    return ld
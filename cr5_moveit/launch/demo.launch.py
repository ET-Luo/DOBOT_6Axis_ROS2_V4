from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    use_ee_camera_arg = DeclareLaunchArgument(
        "use_ee_camera",
        default_value="true",
        description="Enable end-effector camera link in robot description.",
    )
    camera_profile_arg = DeclareLaunchArgument(
        "camera_profile",
        default_value="short",
        description="Camera profile preset: short or long.",
    )
    camera_length_arg = DeclareLaunchArgument(
        "camera_length",
        default_value="-1",
        description="Override camera length in meters; <= 0 uses profile default.",
    )
    camera_width_arg = DeclareLaunchArgument(
        "camera_width",
        default_value="-1",
        description="Override camera width in meters; <= 0 uses profile default.",
    )
    camera_height_arg = DeclareLaunchArgument(
        "camera_height",
        default_value="-1",
        description="Override camera height in meters; <= 0 uses profile default.",
    )
    camera_offset_x_arg = DeclareLaunchArgument(
        "camera_offset_x",
        default_value="0.03",
        description="Camera offset X from Link6 in meters.",
    )
    camera_offset_y_arg = DeclareLaunchArgument(
        "camera_offset_y",
        default_value="0.0",
        description="Camera offset Y from Link6 in meters.",
    )
    camera_offset_z_arg = DeclareLaunchArgument(
        "camera_offset_z",
        default_value="0.06",
        description="Camera offset Z from Link6 in meters.",
    )

    def _launch_setup(context, *args, **kwargs):
        use_ee_camera = LaunchConfiguration("use_ee_camera").perform(context)
        camera_profile = LaunchConfiguration("camera_profile").perform(context).strip().lower()
        camera_length = LaunchConfiguration("camera_length").perform(context)
        camera_width = LaunchConfiguration("camera_width").perform(context)
        camera_height = LaunchConfiguration("camera_height").perform(context)
        camera_offset_x = LaunchConfiguration("camera_offset_x").perform(context)
        camera_offset_y = LaunchConfiguration("camera_offset_y").perform(context)
        camera_offset_z = LaunchConfiguration("camera_offset_z").perform(context)

        profile_dims = {
            "short": (0.06, 0.04, 0.04),
            "long": (0.12, 0.04, 0.04),
        }
        default_length, default_width, default_height = profile_dims.get(camera_profile, profile_dims["short"])

        def resolve_dim(raw_value, fallback):
            try:
                parsed = float(raw_value)
                return str(parsed if parsed > 0.0 else fallback)
            except ValueError:
                return str(fallback)

        resolved_length = resolve_dim(camera_length, default_length)
        resolved_width = resolve_dim(camera_width, default_width)
        resolved_height = resolve_dim(camera_height, default_height)

        print(f"[CR5 Camera Params] profile={camera_profile} length={resolved_length} width={resolved_width} height={resolved_height} offset=({camera_offset_x},{camera_offset_y},{camera_offset_z}) use_ee_camera={use_ee_camera}")
        moveit_config = (
            MoveItConfigsBuilder("cr5_robot", package_name="cr5_moveit")
            .robot_description(
                file_path="config/cr5_robot.urdf.xacro",
                mappings={
                    "use_ee_camera": use_ee_camera,
                    "camera_length": resolved_length,
                    "camera_width": resolved_width,
                    "camera_height": resolved_height,
                    "camera_offset_x": camera_offset_x,
                    "camera_offset_y": camera_offset_y,
                    "camera_offset_z": camera_offset_z,
                },
            )
            .to_moveit_configs()
        )
        return [generate_demo_launch(moveit_config)]

    return LaunchDescription([
        use_ee_camera_arg,
        camera_profile_arg,
        camera_length_arg,
        camera_width_arg,
        camera_height_arg,
        camera_offset_x_arg,
        camera_offset_y_arg,
        camera_offset_z_arg,
        OpaqueFunction(function=_launch_setup),
    ])

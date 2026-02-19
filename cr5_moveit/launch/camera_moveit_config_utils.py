from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder


_PROFILE_DIMS = {
    "short": (0.06, 0.04, 0.04),
    "long": (0.12, 0.04, 0.04),
}


def _resolve_dim(raw_value, fallback):
    try:
        parsed = float(raw_value)
        return str(parsed if parsed > 0.0 else fallback)
    except ValueError:
        return str(fallback)


def build_cr5_moveit_config(context):
    use_ee_camera = LaunchConfiguration("use_ee_camera", default="true").perform(context)
    camera_profile = (
        LaunchConfiguration("camera_profile", default="short").perform(context).strip().lower()
    )
    camera_length = LaunchConfiguration("camera_length", default="-1").perform(context)
    camera_width = LaunchConfiguration("camera_width", default="-1").perform(context)
    camera_height = LaunchConfiguration("camera_height", default="-1").perform(context)
    camera_offset_x = LaunchConfiguration("camera_offset_x", default="0.03").perform(context)
    camera_offset_y = LaunchConfiguration("camera_offset_y", default="0.0").perform(context)
    camera_offset_z = LaunchConfiguration("camera_offset_z", default="0.06").perform(context)

    default_length, default_width, default_height = _PROFILE_DIMS.get(
        camera_profile, _PROFILE_DIMS["short"]
    )
    resolved_length = _resolve_dim(camera_length, default_length)
    resolved_width = _resolve_dim(camera_width, default_width)
    resolved_height = _resolve_dim(camera_height, default_height)

    return (
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


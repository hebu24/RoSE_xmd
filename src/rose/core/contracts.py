PROJECT_NAME = "rose"
POLICY_NAME = "IP"
MAP_INTERFACE = "MAP"
MAP_ACTION_DIM = 7
SUPPORTED_PLATFORMS = ("maniskill", "libero", "franka")


def validate_contract(config: dict) -> None:
    if config.get("project", {}).get("name") != PROJECT_NAME:
        raise ValueError(f"project.name must be {PROJECT_NAME}")
    if config.get("policy", {}).get("name") != POLICY_NAME:
        raise ValueError(f"policy.name must be {POLICY_NAME}")
    if config.get("map", {}).get("interface") != MAP_INTERFACE:
        raise ValueError(f"map.interface must be {MAP_INTERFACE}")
    if config.get("platform") not in SUPPORTED_PLATFORMS:
        raise ValueError(f"unsupported platform: {config.get('platform')}")

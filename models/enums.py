import enum


class RoleType(enum.Enum):
    """
    Enum for the role type.
    """

    ANONYMOUS_VIEWER = "anonymous_viewer"
    SIGNED_CREATOR = "signed_creator"

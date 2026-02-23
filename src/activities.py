"""
Activity management business logic.

This module contains the core functions for managing activity signups and removals.
It's separated from FastAPI endpoints to enable testable, pure business logic.
"""


class ActivityNotFound(Exception):
    """Raised when an activity is not found in the activities collection."""
    pass


class ParticipantNotFound(Exception):
    """Raised when a participant is not found in an activity."""
    pass


def signup_participant(activities: dict, activity_name: str, email: str) -> None:
    """
    Sign up a student for an activity.

    Args:
        activities: The activities dictionary
        activity_name: Name of the activity
        email: Student email address

    Raises:
        ActivityNotFound: If the activity does not exist
        ValueError: If student is already signed up
    """
    # Validate activity exists
    if activity_name not in activities:
        raise ActivityNotFound(f"Activity '{activity_name}' not found")

    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise ValueError("Student already signed up")

    # Add student
    activity["participants"].append(email)


def unregister_participant(activities: dict, activity_name: str, email: str) -> None:
    """
    Unregister a student from an activity.

    Args:
        activities: The activities dictionary
        activity_name: Name of the activity
        email: Student email address

    Raises:
        ActivityNotFound: If the activity does not exist
        ParticipantNotFound: If the participant is not signed up for this activity
    """
    # Validate activity exists
    if activity_name not in activities:
        raise ActivityNotFound(f"Activity '{activity_name}' not found")

    activity = activities[activity_name]

    # Validate participant exists
    if email not in activity["participants"]:
        raise ParticipantNotFound(
            f"Participant '{email}' not found in '{activity_name}'"
        )

    activity["participants"].remove(email)

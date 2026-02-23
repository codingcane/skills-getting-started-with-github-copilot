"""
Unit tests for activity management business logic.

Tests cover signup and unregister operations, including error cases.
"""

import pytest
from src.activities import (
    signup_participant,
    unregister_participant,
    ActivityNotFound,
    ParticipantNotFound,
)


class TestSignupParticipant:
    """Tests for signup_participant function."""

    @pytest.fixture
    def sample_activities(self):
        """Fixture providing sample activities for testing."""
        return {
            "Chess Club": {
                "description": "Learn chess strategies",
                "schedule": "Friday 3:30 PM",
                "max_participants": 12,
                "participants": ["alice@school.edu"],
            },
            "Basketball": {
                "description": "Play basketball",
                "schedule": "Monday 4:00 PM",
                "max_participants": 15,
                "participants": [],
            },
        }

    def test_signup_successful(self, sample_activities):
        """Test successful signup to an activity."""
        signup_participant(sample_activities, "Chess Club", "bob@school.edu")
        assert "bob@school.edu" in sample_activities["Chess Club"]["participants"]
        assert len(sample_activities["Chess Club"]["participants"]) == 2

    def test_signup_to_empty_activity(self, sample_activities):
        """Test signup to an activity with no participants."""
        signup_participant(sample_activities, "Basketball", "charlie@school.edu")
        assert "charlie@school.edu" in sample_activities["Basketball"]["participants"]
        assert len(sample_activities["Basketball"]["participants"]) == 1

    def test_signup_activity_not_found(self, sample_activities):
        """Test signup to a non-existent activity raises ActivityNotFound."""
        with pytest.raises(ActivityNotFound):
            signup_participant(sample_activities, "Yoga Club", "dave@school.edu")

    def test_signup_duplicate_student(self, sample_activities):
        """Test signup prevents duplicate registrations."""
        with pytest.raises(ValueError, match="already signed up"):
            signup_participant(sample_activities, "Chess Club", "alice@school.edu")

    def test_signup_multiple_students(self, sample_activities):
        """Test multiple students can sign up for the same activity."""
        signup_participant(sample_activities, "Basketball", "eve@school.edu")
        signup_participant(sample_activities, "Basketball", "frank@school.edu")
        assert len(sample_activities["Basketball"]["participants"]) == 2
        assert "eve@school.edu" in sample_activities["Basketball"]["participants"]
        assert "frank@school.edu" in sample_activities["Basketball"]["participants"]

    def test_signup_student_in_multiple_activities(self, sample_activities):
        """Test a student can sign up for multiple activities."""
        student = "grace@school.edu"
        signup_participant(sample_activities, "Chess Club", student)
        signup_participant(sample_activities, "Basketball", student)
        assert student in sample_activities["Chess Club"]["participants"]
        assert student in sample_activities["Basketball"]["participants"]


class TestUnregisterParticipant:
    """Tests for unregister_participant function."""

    @pytest.fixture
    def sample_activities(self):
        """Fixture providing sample activities for testing."""
        return {
            "Chess Club": {
                "description": "Learn chess strategies",
                "schedule": "Friday 3:30 PM",
                "max_participants": 12,
                "participants": ["alice@school.edu", "bob@school.edu"],
            },
            "Basketball": {
                "description": "Play basketball",
                "schedule": "Monday 4:00 PM",
                "max_participants": 15,
                "participants": ["charlie@school.edu"],
            },
        }

    def test_unregister_successful(self, sample_activities):
        """Test successful unregistration from an activity."""
        unregister_participant(sample_activities, "Chess Club", "alice@school.edu")
        assert "alice@school.edu" not in sample_activities["Chess Club"]["participants"]
        assert len(sample_activities["Chess Club"]["participants"]) == 1

    def test_unregister_only_participant(self, sample_activities):
        """Test unregistering the only participant from an activity."""
        unregister_participant(sample_activities, "Basketball", "charlie@school.edu")
        assert (
            len(sample_activities["Basketball"]["participants"]) == 0
        )

    def test_unregister_activity_not_found(self, sample_activities):
        """Test unregister from non-existent activity raises ActivityNotFound."""
        with pytest.raises(ActivityNotFound):
            unregister_participant(sample_activities, "Yoga Club", "alice@school.edu")

    def test_unregister_participant_not_found(self, sample_activities):
        """Test unregister non-existent participant raises ParticipantNotFound."""
        with pytest.raises(ParticipantNotFound):
            unregister_participant(sample_activities, "Chess Club", "unknown@school.edu")

    def test_unregister_already_removed_participant(self, sample_activities):
        """Test unregister of already removed participant raises ParticipantNotFound."""
        unregister_participant(sample_activities, "Chess Club", "alice@school.edu")
        with pytest.raises(ParticipantNotFound):
            unregister_participant(sample_activities, "Chess Club", "alice@school.edu")

    def test_unregister_participant_from_another_activity(self, sample_activities):
        """Test unregister of participant not in specified activity."""
        with pytest.raises(ParticipantNotFound):
            unregister_participant(sample_activities, "Basketball", "alice@school.edu")


class TestSignupUnregisterIntegration:
    """Integration tests combining signup and unregister operations."""

    @pytest.fixture
    def sample_activities(self):
        """Fixture providing sample activities for testing."""
        return {
            "Chess Club": {
                "description": "Learn chess strategies",
                "schedule": "Friday 3:30 PM",
                "max_participants": 12,
                "participants": [],
            },
        }

    def test_signup_then_unregister(self, sample_activities):
        """Test signup followed by unregister returns activity to empty state."""
        activity_name = "Chess Club"
        student = "henry@school.edu"

        signup_participant(sample_activities, activity_name, student)
        assert student in sample_activities[activity_name]["participants"]

        unregister_participant(sample_activities, activity_name, student)
        assert student not in sample_activities[activity_name]["participants"]
        assert len(sample_activities[activity_name]["participants"]) == 0

    def test_multiple_signups_and_unregisters(self, sample_activities):
        """Test multiple students signing up and unregistering."""
        activity_name = "Chess Club"
        students = ["iris@school.edu", "jack@school.edu", "kate@school.edu"]

        for student in students:
            signup_participant(sample_activities, activity_name, student)

        assert len(sample_activities[activity_name]["participants"]) == 3

        unregister_participant(sample_activities, activity_name, students[0])
        assert len(sample_activities[activity_name]["participants"]) == 2
        assert students[0] not in sample_activities[activity_name]["participants"]

        signup_participant(sample_activities, activity_name, students[0])
        assert len(sample_activities[activity_name]["participants"]) == 3

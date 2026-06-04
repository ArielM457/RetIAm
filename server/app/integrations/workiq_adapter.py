from app.core.config import get_settings


def workiq_enabled() -> bool:
    settings = get_settings()
    return bool(
        settings.workiq_tenant_id
        and settings.workiq_client_id
        and settings.workiq_client_secret
    )


def get_mock_calendar_context(preferred_time: str | None, weekly_hours: int | None) -> dict:
    preferred_block = preferred_time or "morning"
    windows = {
        "morning": ["07:30-08:30", "08:45-09:30"],
        "afternoon": ["13:30-14:30", "15:00-16:00"],
        "night": ["18:30-19:30", "20:00-21:00"],
    }
    recommended_days = {
        "morning": ["Monday", "Thursday", "Friday"],
        "afternoon": ["Tuesday", "Thursday", "Friday"],
        "night": ["Monday", "Wednesday", "Saturday"],
    }
    return {
        "provider": "mock",
        "preferred_time": preferred_block,
        "meeting_hours_week": 12,
        "focus_windows": [
            f"{preferred_block} block 1",
            f"{preferred_block} block 2",
        ],
        "recommended_study_days": recommended_days[preferred_block],
        "avoid_days": ["Wednesday"],
        "meeting_density_by_day": {
            "Monday": "medium",
            "Tuesday": "medium",
            "Wednesday": "high",
            "Thursday": "low",
            "Friday": "low",
        },
        "preferred_delivery_windows": windows[preferred_block],
        "deadline_alert_offsets_days": [7, 3, 0],
        "weekly_hours_available": weekly_hours or 4,
    }

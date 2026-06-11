from app.core.config import get_settings


def workiq_enabled() -> bool:
    settings = get_settings()
    return bool(
        settings.workiq_tenant_id
        and settings.workiq_client_id
        and settings.workiq_client_secret
    )


def get_mock_calendar_context(
    preferred_time: str | None,
    weekly_hours: int | None,
    preferred_start_hour: int | None = None,
    preferred_study_days: list[str] | None = None,
) -> dict:
    preferred_block = preferred_time or "morning"
    default_windows = {
        "morning": ["07:30-09:30"],
        "afternoon": ["13:30-15:30"],
        "night": ["18:30-20:30"],
    }
    recommended_days = {
        "morning": ["Monday", "Thursday", "Friday"],
        "afternoon": ["Tuesday", "Thursday", "Friday"],
        "night": ["Monday", "Wednesday", "Saturday"],
    }
    hour = preferred_start_hour
    if hour is None:
        hour = {"morning": 8, "afternoon": 14, "night": 19}[preferred_block]
    start_label = f"{hour:02d}:00"
    end_label = f"{min(hour + 2, 23):02d}:00"
    windows = [f"{start_label}-{end_label}"]
    chosen_days = preferred_study_days or recommended_days[preferred_block]
    return {
        "provider": "mock",
        "preferred_time": preferred_block,
        "preferred_start_hour": hour,
        "meeting_hours_week": 12,
        "focus_windows": [
            f"{preferred_block} desde {start_label}",
        ],
        "recommended_study_days": chosen_days,
        "avoid_days": ["Wednesday"],
        "meeting_density_by_day": {
            "Monday": "medium",
            "Tuesday": "medium",
            "Wednesday": "high",
            "Thursday": "low",
            "Friday": "low",
        },
        "preferred_delivery_windows": windows or default_windows[preferred_block],
        "deadline_alert_offsets_days": [7, 3, 0],
        "weekly_hours_available": weekly_hours or 4,
    }

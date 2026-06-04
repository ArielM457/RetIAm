from typing import Literal

from pydantic import BaseModel, Field


Difficulty = Literal["basic", "intermediate", "advanced"]
PreferredTime = Literal["morning", "afternoon", "night"]
LearningStyle = Literal["documentation", "code_examples", "hands_on", "mixed"]


class OnboardingQuestionOption(BaseModel):
    key: str
    label: str


class OnboardingQuestion(BaseModel):
    id: str
    prompt: str
    topic: str
    difficulty: Difficulty
    options: list[OnboardingQuestionOption]


class OnboardingQuestionsResponse(BaseModel):
    track: str
    target_certification: str
    questions: list[OnboardingQuestion]


class OnboardingAnswerSubmission(BaseModel):
    question_id: str
    selected_option_key: str


class OnboardingEvaluationRequest(BaseModel):
    professional_role: str
    target_certification: str
    weekly_hours_available: int = Field(ge=1, le=40)
    preferred_time: PreferredTime
    learning_style: list[LearningStyle] = Field(min_length=1, max_length=4)
    answers: list[OnboardingAnswerSubmission] = Field(min_length=5, max_length=10)


class OnboardingAnswerResult(BaseModel):
    question_id: str
    selected_option_key: str
    correct_option_key: str
    is_correct: bool
    difficulty: Difficulty
    topic: str


class LearningProfileSnapshot(BaseModel):
    professional_role: str
    target_certification: str
    detected_level: Difficulty
    weekly_hours_available: int
    preferred_time: PreferredTime
    learning_style: list[LearningStyle]
    profile_version: int
    onboarding_completed_at: str | None = None


class OnboardingEvaluationResponse(BaseModel):
    profile: LearningProfileSnapshot
    score: int
    max_score: int
    answer_results: list[OnboardingAnswerResult]
    summary: str
    recommendations: list[str]


class SavedAssessmentResponse(BaseModel):
    id: str
    user_id: str
    professional_role: str
    target_certification: str
    detected_level: Difficulty
    weekly_hours_available: int
    preferred_time: PreferredTime
    learning_style: list[LearningStyle]
    score: int
    max_score: int
    notes: str | None = None
    created_at: str

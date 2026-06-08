from pydantic import BaseModel, Field


class ExamQuestion(BaseModel):
    question_id: str
    prompt: str
    options: list[str] = Field(default_factory=list)
    correct_option_index: int
    source: str
    section_id: str


class ExamQuestionPublic(BaseModel):
    """Pregunta de examen sin la respuesta correcta (lo que ve el cliente)."""

    question_id: str
    prompt: str
    options: list[str] = Field(default_factory=list)
    source: str
    section_id: str


class StartFinalExamRequest(BaseModel):
    plan_id: str
    time_limit_minutes: int = Field(default=60, ge=30, le=180)


class FinalExamAttemptResponse(BaseModel):
    id: str | None = None
    plan_id: str
    target_certification: str
    questions: list[ExamQuestionPublic] = Field(default_factory=list)
    time_limit_minutes: int = 60
    score: int = 0
    max_score: int = 0
    passed: bool = False
    failed_sections: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    next_certification: str | None = None
    certificate_id: str | None = None
    started_at: str | None = None
    submitted_at: str | None = None


class SubmitFinalExamRequest(BaseModel):
    answers: list[dict] = Field(default_factory=list)


class CertificateResponse(BaseModel):
    id: str
    user_id: str
    recipient_name: str | None = None
    target_certification: str
    score: int
    pdf_url: str | None = None
    verification_code: str
    issued_at: str


class CertificateVerificationResponse(BaseModel):
    valid: bool
    certificate_id: str | None = None
    recipient_name: str | None = None
    target_certification: str | None = None
    score: int | None = None
    issued_at: str | None = None

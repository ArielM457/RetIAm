import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { runtimeConfig } from '../config/runtime-config';

export type UserProfile = {
  id: string;
  email: string;
  full_name: string | null;
  role: 'manager' | 'employee';
  professional_role: string | null;
  org_id: string | null;
  team_id: string | null;
  target_certification: string | null;
  detected_level: string | null;
  weekly_hours_available: number | null;
  preferred_time: string | null;
  learning_style: string[];
  profile_version: number;
  onboarding_completed_at: string | null;
};

export type EmailValidationResponse = {
  email: string;
  is_valid: boolean;
  is_corporate_domain: boolean;
  should_recommend_custom_domain: boolean;
  recommendation: string | null;
  message: string;
};

export type AuthUserSummary = {
  id: string;
  email: string;
  full_name: string | null;
  role: 'manager' | 'employee';
  org_id: string | null;
  team_id: string | null;
};

export type AuthSessionResponse = {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  expires_at: number | null;
  user: AuthUserSummary;
  message: string;
};

export type OnboardingQuestionOption = {
  key: string;
  label: string;
};

export type OnboardingQuestion = {
  id: string;
  prompt: string;
  topic: string;
  difficulty: 'basic' | 'intermediate' | 'advanced';
  options: OnboardingQuestionOption[];
};

export type OnboardingQuestionsResponse = {
  track: string;
  target_certification: string;
  questions: OnboardingQuestion[];
};

export type OnboardingEvaluationPayload = {
  professional_role: string;
  target_certification: string;
  weekly_hours_available: number;
  preferred_time: 'morning' | 'afternoon' | 'night';
  learning_style: Array<'documentation' | 'code_examples' | 'hands_on' | 'mixed'>;
  answers: Array<{ question_id: string; selected_option_key: string }>;
};

export type OnboardingEvaluationResponse = {
  profile: {
    professional_role: string;
    target_certification: string;
    detected_level: string;
    weekly_hours_available: number;
    preferred_time: string;
    learning_style: string[];
    profile_version: number;
    onboarding_completed_at: string | null;
  };
  score: number;
  max_score: number;
  summary: string;
  recommendations: string[];
  answer_results: Array<{
    question_id: string;
    selected_option_key: string;
    correct_option_key: string;
    is_correct: boolean;
    difficulty: string;
    topic: string;
  }>;
};

export type SavedAssessmentResponse = {
  id: string;
  user_id: string;
  professional_role: string;
  target_certification: string;
  detected_level: string;
  weekly_hours_available: number;
  preferred_time: string;
  learning_style: string[];
  score: number;
  max_score: number;
  notes: string | null;
  questions: Array<Record<string, unknown>>;
  answers: Array<{
    key?: string;
    title?: string;
    answer?: string;
    question_id?: string;
    selected_option_key?: string;
    correct_option_key?: string;
    is_correct?: boolean;
    difficulty?: string;
    topic?: string;
  }>;
  created_at: string;
};

export type AgentIntakeResponse = {
  summary: string;
  saved_answers: number;
  onboarding_completed_at: string;
};

export type AgentIntakeAssistResponse = {
  message: string;
  should_advance: boolean;
  normalized_answer: string | null;
  extracted_answers: Record<string, string>;
};

export type CertificationSummary = {
  code: string;
  title: string;
  provider: string;
  level: string;
  description: string;
  recommended_for: string[];
};

export type ResourceReference = {
  title: string;
  type: string;
  source: string;
  url: string;
};

export type LessonSource = {
  title: string;
  url: string | null;
  source: string | null;
};

export type CourseLesson = {
  id: string | null;
  section_id?: string | null;
  lesson_key: string;
  title: string;
  order: number;
  duration_minutes: number;
  content_md: string | null;
  learning_objectives: string[];
  sources: LessonSource[];
};

export type CourseLab = {
  id: string | null;
  lab_key: string;
  title: string;
  is_optional: boolean;
  estimated_minutes: number;
  instructions_md: string | null;
  rubric: Array<{ criterion: string; weight: number; description?: string | null }>;
};

export type RouteSection = {
  section_id: string;
  title: string;
  order: number;
  estimated_hours: number;
  resources: ResourceReference[];
  prerequisite_sections: string[];
  duration_minutes: number;
  course_section_id: string | null;
  lessons: CourseLesson[];
  labs: CourseLab[];
};

export type CourseCatalogSummary = {
  id: string | null;
  certification_code: string;
  track: string;
  title: string;
  summary: string | null;
  provider: string | null;
  level: string;
  total_duration_minutes: number;
  section_count: number;
  lesson_count: number;
};

export type CourseSectionContent = {
  id: string | null;
  course_id: string | null;
  section_key: string;
  title: string;
  summary: string | null;
  order: number;
  duration_minutes: number;
  lessons: CourseLesson[];
  labs: CourseLab[];
};

export type CourseDetail = {
  id: string | null;
  certification_code: string;
  track: string;
  title: string;
  summary: string | null;
  provider: string | null;
  level: string;
  total_duration_minutes: number;
  source: string;
  source_url: string | null;
  sections: CourseSectionContent[];
};

export type QuizQuestionPublic = {
  question_id: string;
  prompt: string;
  options: string[];
  source: string;
  section_id?: string | null;
};

export type RankingMember = {
  user_id: string;
  full_name: string;
  rank: number;
  score: number;
  progress_percent: number;
  completed_sessions: number;
  study_minutes: number;
  fastest_minutes: number | null;
  avg_minutes: number | null;
  exams_taken: number;
  exams_passed: number;
  pass_rate: number;
  learning_style: string[];
};

export type MethodologyStat = { style: string; avg_progress: number; members: number };

export type TeamRanking = {
  team_id: string;
  team_name: string | null;
  members: RankingMember[];
  record_holder: RankingMember | null;
  best_methodology: MethodologyStat | null;
  methodology_breakdown: MethodologyStat[];
  narrative: string;
};

export type CustomCourseSectionSummary = {
  title: string;
  lessons: string[];
  labs: string[];
};

export type CustomCourseResult = {
  certification_code: string;
  title: string;
  summary: string | null;
  level: string;
  total_duration_minutes: number;
  section_count: number;
  lesson_count: number;
  lab_count: number;
  is_certifiable: boolean;
  issues: string[];
  exam_questions: number;
  exam_pass_percent: number;
  sections: CustomCourseSectionSummary[];
  chunk_count?: number;
  message?: string;
};

export type PresentationSlide = {
  title: string;
  bullets: string[];
  code: string | null;
  diagram: string[];
  narration: string;
};

export type PresentationResponse = {
  course_code: string;
  topic: string;
  title: string;
  grounded: boolean;
  slides: PresentationSlide[];
  sources: LessonSource[];
  source_mode: string;
  message: string | null;
};

export type LessonChatMessage = {
  id: string | null;
  role: 'user' | 'assistant';
  content: string;
  sources: LessonSource[];
  suggested_questions: string[];
  source_mode: string;
  created_at: string | null;
};

export type LessonChatResponse = {
  lesson_id: string;
  answer: LessonChatMessage;
  history: LessonChatMessage[];
};

export type SuggestedQuestionsResponse = {
  lesson_id: string;
  questions: string[];
  source_mode: string;
};

export type CompleteLessonResponse = {
  lesson_id: string;
  status: string;
  completed_lessons: number;
  total_lessons: number;
  progress_percent: number;
  insight_note: string | null;
  coach_message: string | null;
  coach_scheduled_for: string | null;
  next_action: 'continue' | 'final_exam' | string;
  next_action_label: string | null;
  source_mode: string;
};

export type CertificateVerificationResponse = {
  valid: boolean;
  certificate_id: string | null;
  recipient_name: string | null;
  target_certification: string | null;
  score: number | null;
  issued_at: string | null;
};

export type CertificationRouteResponse = {
  id: string | null;
  target_certification: string;
  detected_level: string;
  source_mode: string;
  sections: RouteSection[];
};

export type StudyPlanResponse = {
  id: string | null;
  route_id: string;
  target_certification: string;
  deadline_at: string;
  weekly_hours: number;
  weekly_milestones: Array<{
    week: number;
    title: string;
    section_ids: string[];
    estimated_hours: number;
  }>;
  workiq_context: Record<string, unknown>;
  status: string;
};

export type TeamSummary = {
  id: string;
  name: string;
  org_id: string;
  manager_id: string;
  organization_name: string | null;
  sector: string | null;
  member_capacity: number | null;
  work_style: string | null;
  notes: string | null;
  member_count: number;
  pending_invites: number;
};

export type TeamAccessCodeSummary = {
  id: string;
  team_id: string;
  org_id: string;
  code: string;
  role: 'manager' | 'employee';
  status: 'active' | 'used' | 'expired' | 'cancelled';
  created_by: string;
  used_by: string | null;
  expires_at: string;
  created_at: string | null;
  used_at: string | null;
};

export type TeamMemberSummary = {
  user_id: string;
  full_name: string | null;
  email: string;
  role: 'manager' | 'employee';
  certification: string | null;
  team_id: string | null;
};

export type SessionEvaluation = {
  mandatory_answer?: { submitted_answer: string; is_correct: boolean; feedback: string };
  quiz_questions?: QuizQuestionPublic[];
  quiz_source_mode?: string;
  quiz?: {
    score: number;
    passed: boolean;
    total_questions: number;
    correct_answers?: number;
    source_mode?: string;
  };
  lab?: {
    score: number;
    passed: boolean;
    feedback: string;
    criteria?: Record<string, number>;
    source_mode?: string;
  };
};

export type ManagerSetupAgentAssistResponse = {
  message: string;
  should_advance: boolean;
  normalized_answer: string | null;
};

export type LearningSessionResponse = {
  id: string | null;
  plan_id: string;
  section_id: string;
  section_title: string;
  session_type: string;
  status: string;
  resources: ResourceReference[];
  mandatory_question: {
    prompt: string;
    answer: string;
    source: string;
  } | null;
  free_questions: Array<{ question: string; answer: string; source: string; source_mode?: string }>;
  evaluation: SessionEvaluation;
  survey: Record<string, unknown> | null;
  started_at: string | null;
  completed_at: string | null;
};

export type ReminderResponse = {
  id: string | null;
  kind: string;
  tone: string;
  delivery_channel: string;
  message: string;
  scheduled_for: string;
  status: string;
};

export type ReminderGenerationResponse = {
  reminders: ReminderResponse[];
  workiq_context: Record<string, unknown>;
};

export type CertificateResponse = {
  id: string;
  user_id: string;
  recipient_name: string | null;
  target_certification: string;
  score: number;
  pdf_url: string | null;
  verification_code: string;
  issued_at: string;
};

export type FinalExamAttemptResponse = {
  id: string | null;
  plan_id: string;
  target_certification: string;
  questions: Array<{
    question_id: string;
    prompt: string;
    options: string[];
    correct_option_index: number;
    source: string;
    section_id: string;
  }>;
  time_limit_minutes: number;
  score: number;
  max_score: number;
  passed: boolean;
  failed_sections: string[];
  recommendations: string[];
  next_certification: string | null;
  certificate_id: string | null;
  started_at: string | null;
  submitted_at: string | null;
};

export type ManagerDashboardResponse = {
  team_id: string;
  team_name: string;
  organization_name: string | null;
  sector: string | null;
  member_capacity: number | null;
  work_style: string | null;
  team_progress_percent: number;
  top_gaps: string[];
  members: Array<{
    user_id: string;
    full_name: string | null;
    certification: string | null;
    progress_percent: number;
    days_to_deadline: number | null;
    risk_status: string;
  }>;
};

export type ManagerMemberDetailResponse = {
  user_id: string;
  full_name: string | null;
  email: string | null;
  professional_role: string | null;
  certification: string | null;
  detected_level: string | null;
  preferred_time: string | null;
  learning_style: string[];
  recommended_study_pattern: string | null;
  progress_percent: number;
  completed_sessions: number;
  completed_certifications: number;
  days_to_deadline: number | null;
  risk_status: string;
  pending_sections: string[];
};

export type WeeklyTeamSummaryResponse = {
  team_id: string;
  team_name: string;
  summary_date: string;
  delivery_channel: string;
  highlights: string[];
  risks: string[];
  upcoming_deadlines: Array<{
    user_id: string;
    full_name: string | null;
    certification: string | null;
    progress_percent: number;
    days_to_deadline: number | null;
    risk_status: string;
  }>;
};

export type SuggestionResponse = {
  id: string | null;
  category: string;
  message: string;
  status: string;
  agent_response: string;
  created_at: string | null;
};

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = runtimeConfig.apiBaseUrl;

  validateEmail(email: string): Promise<EmailValidationResponse> {
    return firstValueFrom(
      this.http.post<EmailValidationResponse>(`${this.apiBaseUrl}/auth/validate-email`, { email }),
    );
  }

  register(payload: {
    email: string;
    password: string;
    full_name?: string;
    role?: 'manager' | 'employee';
    team_access_code?: string;
  }): Promise<AuthSessionResponse> {
    return firstValueFrom(
      this.http.post<AuthSessionResponse>(`${this.apiBaseUrl}/auth/register`, payload),
    );
  }

  login(payload: { email: string; password: string }): Promise<AuthSessionResponse> {
    return firstValueFrom(
      this.http.post<AuthSessionResponse>(`${this.apiBaseUrl}/auth/login`, payload),
    );
  }

  getCurrentProfile(): Promise<UserProfile> {
    return firstValueFrom(this.http.get<UserProfile>(`${this.apiBaseUrl}/users/me`));
  }

  updateCurrentProfile(payload: Partial<UserProfile>): Promise<UserProfile> {
    return firstValueFrom(this.http.patch<UserProfile>(`${this.apiBaseUrl}/users/me`, payload));
  }

  getOnboardingQuestions(targetCertification: string): Promise<OnboardingQuestionsResponse> {
    return firstValueFrom(
      this.http.get<OnboardingQuestionsResponse>(
        `${this.apiBaseUrl}/users/me/onboarding/questions`,
        {
          params: { target_certification: targetCertification },
        },
      ),
    );
  }

  evaluateOnboarding(payload: OnboardingEvaluationPayload): Promise<OnboardingEvaluationResponse> {
    return firstValueFrom(
      this.http.post<OnboardingEvaluationResponse>(
        `${this.apiBaseUrl}/users/me/onboarding/evaluate`,
        payload,
      ),
    );
  }

  getLatestAssessment(): Promise<SavedAssessmentResponse | null> {
    return firstValueFrom(
      this.http.get<SavedAssessmentResponse | null>(
        `${this.apiBaseUrl}/users/me/onboarding/latest`,
      ),
    );
  }

  saveAgentIntake(payload: {
    professional_role: string;
    weekly_hours_available: number;
    preferred_time: 'morning' | 'afternoon' | 'night';
    learning_style: string[];
    target_certification?: string | null;
    answers: Array<{ key: string; title: string; answer: string }>;
  }): Promise<AgentIntakeResponse> {
    return firstValueFrom(
      this.http.post<AgentIntakeResponse>(`${this.apiBaseUrl}/users/me/onboarding/intake`, payload),
    );
  }

  assistAgentIntake(payload: {
    question_key: string;
    question_title: string;
    question_prompt: string;
    user_message: string;
    collected_answers: Record<string, string>;
  }): Promise<AgentIntakeAssistResponse> {
    return firstValueFrom(
      this.http.post<AgentIntakeAssistResponse>(`${this.apiBaseUrl}/users/me/onboarding/assist`, payload),
    );
  }

  listCertifications(): Promise<CertificationSummary[]> {
    return firstValueFrom(this.http.get<CertificationSummary[]>(`${this.apiBaseUrl}/certifications`));
  }

  generateRoute(targetCertification: string): Promise<CertificationRouteResponse> {
    return firstValueFrom(
      this.http.post<CertificationRouteResponse>(`${this.apiBaseUrl}/learning/routes`, {
        target_certification: targetCertification,
      }),
    );
  }

  getLatestRoute(): Promise<CertificationRouteResponse | null> {
    return firstValueFrom(
      this.http.get<CertificationRouteResponse | null>(`${this.apiBaseUrl}/learning/routes/latest`),
    );
  }

  generatePlan(payload: {
    route_id: string;
    weekly_hours?: number;
    preferred_time?: string;
    requested_deadline?: string;
  }): Promise<StudyPlanResponse> {
    return firstValueFrom(
      this.http.post<StudyPlanResponse>(`${this.apiBaseUrl}/learning/plans`, payload),
    );
  }

  getLatestPlan(): Promise<StudyPlanResponse | null> {
    return firstValueFrom(
      this.http.get<StudyPlanResponse | null>(`${this.apiBaseUrl}/learning/plans/latest`),
    );
  }

  listTeams(): Promise<TeamSummary[]> {
    return firstValueFrom(this.http.get<TeamSummary[]>(`${this.apiBaseUrl}/teams`));
  }

  createTeam(payload: {
    team_name: string;
    organization_name?: string;
    organization_id?: string;
    sector?: string;
    member_capacity?: number;
    work_style?: string;
    notes?: string;
    member_emails?: string[];
  }): Promise<TeamSummary> {
    return firstValueFrom(this.http.post<TeamSummary>(`${this.apiBaseUrl}/teams`, payload));
  }

  createTeamAccessCode(teamId: string, role: 'manager' | 'employee' = 'employee') {
    return firstValueFrom(
      this.http.post<TeamAccessCodeSummary>(`${this.apiBaseUrl}/teams/${teamId}/access-code`, {
        role,
      }),
    );
  }

  joinTeamWithCode(code: string): Promise<TeamSummary> {
    return firstValueFrom(
      this.http.post<TeamSummary>(`${this.apiBaseUrl}/teams/join-with-code`, { code }),
    );
  }

  listTeamMembers(teamId: string): Promise<TeamMemberSummary[]> {
    return firstValueFrom(
      this.http.get<TeamMemberSummary[]>(`${this.apiBaseUrl}/teams/${teamId}/members`),
    );
  }

  inviteTeamMembers(teamId: string, emails: string[], role: 'manager' | 'employee' = 'employee') {
    return firstValueFrom(
      this.http.post(`${this.apiBaseUrl}/teams/${teamId}/invites`, {
        emails,
        role,
      }),
    );
  }

  assistManagerSetup(payload: {
    question_key: string;
    question_title: string;
    question_prompt: string;
    user_message: string;
    collected_answers: Record<string, string>;
  }): Promise<ManagerSetupAgentAssistResponse> {
    return firstValueFrom(
      this.http.post<ManagerSetupAgentAssistResponse>(
        `${this.apiBaseUrl}/teams/setup-agent/assist`,
        payload,
      ),
    );
  }

  assignCertificationToTeam(teamId: string, targetCertification: string, memberIds: string[]) {
    return firstValueFrom(
      this.http.post(`${this.apiBaseUrl}/learning/teams/${teamId}/assignments`, {
        target_certification: targetCertification,
        member_ids: memberIds,
      }),
    );
  }

  startSession(payload: {
    plan_id: string;
    section_id: string;
    section_title: string;
    session_type: 'theory' | 'practice' | 'quiz' | 'lab';
  }): Promise<LearningSessionResponse> {
    return firstValueFrom(
      this.http.post<LearningSessionResponse>(`${this.apiBaseUrl}/sessions`, payload),
    );
  }

  getSession(sessionId: string): Promise<LearningSessionResponse> {
    return firstValueFrom(
      this.http.get<LearningSessionResponse>(`${this.apiBaseUrl}/sessions/${sessionId}`),
    );
  }

  submitMandatoryAnswer(sessionId: string, answer: string): Promise<LearningSessionResponse> {
    return firstValueFrom(
      this.http.post<LearningSessionResponse>(
        `${this.apiBaseUrl}/sessions/${sessionId}/mandatory-answer`,
        { answer },
      ),
    );
  }

  askFreeQuestion(sessionId: string, question: string): Promise<LearningSessionResponse> {
    return firstValueFrom(
      this.http.post<LearningSessionResponse>(
        `${this.apiBaseUrl}/sessions/${sessionId}/free-question`,
        { question },
      ),
    );
  }

  submitEvaluation(
    sessionId: string,
    payload: {
      quiz_answers?: Array<{ question_id: string; selected_option_index: number }>;
      lab_solution_summary?: string;
    },
  ): Promise<LearningSessionResponse> {
    return firstValueFrom(
      this.http.post<LearningSessionResponse>(
        `${this.apiBaseUrl}/sessions/${sessionId}/evaluation`,
        payload,
      ),
    );
  }

  // --- Catalogo de cursos ---
  listCourses(): Promise<CourseCatalogSummary[]> {
    return firstValueFrom(this.http.get<CourseCatalogSummary[]>(`${this.apiBaseUrl}/courses`));
  }

  getCourse(certificationCode: string): Promise<CourseDetail> {
    return firstValueFrom(
      this.http.get<CourseDetail>(`${this.apiBaseUrl}/courses/${encodeURIComponent(certificationCode)}`),
    );
  }

  // --- Tutor por leccion (Gini Eval) ---
  askTutor(sessionId: string, lessonId: string, question: string): Promise<LessonChatResponse> {
    return firstValueFrom(
      this.http.post<LessonChatResponse>(
        `${this.apiBaseUrl}/sessions/${sessionId}/lessons/${lessonId}/chat`,
        { question },
      ),
    );
  }

  getLessonChat(sessionId: string, lessonId: string): Promise<LessonChatMessage[]> {
    return firstValueFrom(
      this.http.get<LessonChatMessage[]>(
        `${this.apiBaseUrl}/sessions/${sessionId}/lessons/${lessonId}/chat`,
      ),
    );
  }

  getSuggestedQuestions(sessionId: string, lessonId: string): Promise<SuggestedQuestionsResponse> {
    return firstValueFrom(
      this.http.get<SuggestedQuestionsResponse>(
        `${this.apiBaseUrl}/sessions/${sessionId}/lessons/${lessonId}/suggested-questions`,
      ),
    );
  }

  // --- Sala de Auxiliaturas (Sala 1): presentaciones ---
  createPresentation(courseCode: string, topic: string): Promise<PresentationResponse> {
    return firstValueFrom(
      this.http.post<PresentationResponse>(`${this.apiBaseUrl}/presentations`, {
        course_code: courseCode,
        topic,
      }),
    );
  }

  /** Duda durante la clase (no regenera la presentación). */
  askPresentation(
    question: string,
    courseCode?: string,
    topic?: string,
  ): Promise<{ answer: string; sources: LessonSource[] }> {
    return firstValueFrom(
      this.http.post<{ answer: string; sources: LessonSource[] }>(
        `${this.apiBaseUrl}/presentations/ask`,
        { question, course_code: courseCode || null, topic: topic || null },
      ),
    );
  }

  /** Genera una presentación a partir de un texto/artículo del alumno. */
  createPresentationFromText(text: string, topic?: string): Promise<PresentationResponse> {
    return firstValueFrom(
      this.http.post<PresentationResponse>(`${this.apiBaseUrl}/presentations/from-text`, {
        text,
        topic: topic || null,
      }),
    );
  }

  // --- Voz (TTS) de la Sala de Auxiliaturas con Azure Speech ---
  speechStatus(): Promise<{ enabled: boolean; voice: string }> {
    return firstValueFrom(
      this.http.get<{ enabled: boolean; voice: string }>(`${this.apiBaseUrl}/speech/status`),
    );
  }

  synthesizeSpeech(text: string): Promise<Blob> {
    return firstValueFrom(
      this.http.post(`${this.apiBaseUrl}/speech/tts`, { text }, { responseType: 'blob' }),
    );
  }

  // --- Tutor por leccion SIN sesion (pagina de lectura del curso) ---
  askLessonTutor(lessonId: string, question: string): Promise<LessonChatResponse> {
    return firstValueFrom(
      this.http.post<LessonChatResponse>(`${this.apiBaseUrl}/lessons/${lessonId}/chat`, {
        question,
      }),
    );
  }

  getLessonChatByLesson(lessonId: string): Promise<LessonChatMessage[]> {
    return firstValueFrom(
      this.http.get<LessonChatMessage[]>(`${this.apiBaseUrl}/lessons/${lessonId}/chat`),
    );
  }

  getLessonSuggestions(lessonId: string): Promise<SuggestedQuestionsResponse> {
    return firstValueFrom(
      this.http.get<SuggestedQuestionsResponse>(
        `${this.apiBaseUrl}/lessons/${lessonId}/suggested-questions`,
      ),
    );
  }

  completeLesson(sessionId: string, lessonId: string): Promise<CompleteLessonResponse> {
    return firstValueFrom(
      this.http.post<CompleteLessonResponse>(
        `${this.apiBaseUrl}/sessions/${sessionId}/lessons/${lessonId}/complete`,
        {},
      ),
    );
  }

  verifyCertificate(verificationCode: string): Promise<CertificateVerificationResponse> {
    return firstValueFrom(
      this.http.get<CertificateVerificationResponse>(
        `${this.apiBaseUrl}/exams/certificates/verify/${encodeURIComponent(verificationCode)}`,
      ),
    );
  }

  submitSurvey(
    sessionId: string,
    payload: {
      skipped: boolean;
      clarity_score?: number;
      preferred_format?: string;
      improvement_note?: string;
    },
  ): Promise<LearningSessionResponse> {
    return firstValueFrom(
      this.http.post<LearningSessionResponse>(
        `${this.apiBaseUrl}/sessions/${sessionId}/survey`,
        payload,
      ),
    );
  }

  recordIntegrityEvent(sessionId: string, eventType: string, payload: Record<string, unknown>) {
    return firstValueFrom(
      this.http.post(`${this.apiBaseUrl}/sessions/${sessionId}/integrity-event`, {
        event_type: eventType,
        payload,
      }),
    );
  }

  generateReminders(): Promise<ReminderGenerationResponse> {
    return firstValueFrom(
      this.http.post<ReminderGenerationResponse>(`${this.apiBaseUrl}/coach/reminders/generate`, {}),
    );
  }

  listMyReminders(): Promise<ReminderResponse[]> {
    return firstValueFrom(
      this.http.get<ReminderResponse[]>(`${this.apiBaseUrl}/coach/reminders/mine`),
    );
  }

  getManagerDashboard(teamId: string): Promise<ManagerDashboardResponse> {
    return firstValueFrom(
      this.http.get<ManagerDashboardResponse>(
        `${this.apiBaseUrl}/manager/teams/${teamId}/dashboard`,
      ),
    );
  }

  getManagerMemberDetail(teamId: string, memberId: string): Promise<ManagerMemberDetailResponse> {
    return firstValueFrom(
      this.http.get<ManagerMemberDetailResponse>(
        `${this.apiBaseUrl}/manager/teams/${teamId}/members/${memberId}`,
      ),
    );
  }

  sendSupportMessage(teamId: string, memberId: string, message: string) {
    return firstValueFrom(
      this.http.post(`${this.apiBaseUrl}/manager/teams/${teamId}/members/${memberId}/support-message`, {
        message,
      }),
    );
  }

  // --- Ranking del equipo + notificaciones (team lead) ---
  getTeamRanking(teamId: string): Promise<TeamRanking> {
    return firstValueFrom(
      this.http.get<TeamRanking>(`${this.apiBaseUrl}/manager/teams/${teamId}/ranking`),
    );
  }

  nudgeAtRisk(teamId: string): Promise<{ count: number; notified: { full_name: string; message: string }[] }> {
    return firstValueFrom(
      this.http.post<{ count: number; notified: { full_name: string; message: string }[] }>(
        `${this.apiBaseUrl}/manager/teams/${teamId}/nudge-at-risk`,
        {},
      ),
    );
  }

  nudgeMember(teamId: string, memberId: string, message?: string): Promise<{ message: string }> {
    return firstValueFrom(
      this.http.post<{ message: string }>(
        `${this.apiBaseUrl}/manager/teams/${teamId}/members/${memberId}/nudge`,
        { message: message || null },
      ),
    );
  }

  // --- Curso personalizado del equipo (team lead) ---
  previewCustomCourse(teamId: string, markdown: string, title?: string): Promise<CustomCourseResult> {
    return firstValueFrom(
      this.http.post<CustomCourseResult>(
        `${this.apiBaseUrl}/manager/teams/${teamId}/custom-courses/preview`,
        { markdown, title: title || null },
      ),
    );
  }

  createCustomCourse(teamId: string, markdown: string, title?: string): Promise<CustomCourseResult> {
    return firstValueFrom(
      this.http.post<CustomCourseResult>(
        `${this.apiBaseUrl}/manager/teams/${teamId}/custom-courses`,
        { markdown, title: title || null },
      ),
    );
  }

  getWeeklySummary(teamId: string): Promise<WeeklyTeamSummaryResponse> {
    return firstValueFrom(
      this.http.get<WeeklyTeamSummaryResponse>(
        `${this.apiBaseUrl}/manager/teams/${teamId}/weekly-summary`,
      ),
    );
  }

  exportManagerPdf(teamId: string): Promise<{ team_id: string; pdf_url: string; generated_at: string }> {
    return firstValueFrom(
      this.http.get<{ team_id: string; pdf_url: string; generated_at: string }>(
        `${this.apiBaseUrl}/manager/teams/${teamId}/export-pdf`,
      ),
    );
  }

  startFinalExam(planId: string, timeLimitMinutes = 60): Promise<FinalExamAttemptResponse> {
    return firstValueFrom(
      this.http.post<FinalExamAttemptResponse>(`${this.apiBaseUrl}/exams/final`, {
        plan_id: planId,
        time_limit_minutes: timeLimitMinutes,
      }),
    );
  }

  submitFinalExam(
    attemptId: string,
    answers: Array<{ question_id: string; selected_option_index: number }>,
  ): Promise<FinalExamAttemptResponse> {
    return firstValueFrom(
      this.http.post<FinalExamAttemptResponse>(
        `${this.apiBaseUrl}/exams/final/${attemptId}/submit`,
        { answers },
      ),
    );
  }

  listCertificates(): Promise<CertificateResponse[]> {
    return firstValueFrom(
      this.http.get<CertificateResponse[]>(`${this.apiBaseUrl}/exams/certificates/mine`),
    );
  }

  createSuggestion(category: string, message: string): Promise<SuggestionResponse> {
    return firstValueFrom(
      this.http.post<SuggestionResponse>(`${this.apiBaseUrl}/suggestions`, { category, message }),
    );
  }

  listMySuggestions(): Promise<SuggestionResponse[]> {
    return firstValueFrom(
      this.http.get<SuggestionResponse[]>(`${this.apiBaseUrl}/suggestions/mine`),
    );
  }

  getTeamSuggestionSummary(teamId: string): Promise<{ team_id: string; totals_by_category: Record<string, number>; totals_by_status: Record<string, number> }> {
    return firstValueFrom(
      this.http.get<{ team_id: string; totals_by_category: Record<string, number>; totals_by_status: Record<string, number> }>(
        `${this.apiBaseUrl}/suggestions/team/${teamId}/summary`,
      ),
    );
  }
}

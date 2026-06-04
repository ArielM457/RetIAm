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

export type RouteSection = {
  section_id: string;
  title: string;
  order: number;
  estimated_hours: number;
  resources: ResourceReference[];
  prerequisite_sections: string[];
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
  member_count: number;
  pending_invites: number;
};

export type TeamMemberSummary = {
  user_id: string;
  full_name: string | null;
  email: string;
  role: 'manager' | 'employee';
  certification: string | null;
  team_id: string | null;
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
  free_questions: Array<{ question: string; answer: string; source: string }>;
  evaluation: Record<string, unknown>;
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
  certification: string | null;
  detected_level: string | null;
  progress_percent: number;
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

  getLatestAssessment(): Promise<OnboardingEvaluationResponse | null> {
    return firstValueFrom(
      this.http.get<OnboardingEvaluationResponse | null>(
        `${this.apiBaseUrl}/users/me/onboarding/latest`,
      ),
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
    member_emails?: string[];
  }): Promise<TeamSummary> {
    return firstValueFrom(this.http.post<TeamSummary>(`${this.apiBaseUrl}/teams`, payload));
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
    payload: { answers?: Array<{ is_correct: boolean }>; lab_solution_summary?: string },
  ): Promise<LearningSessionResponse> {
    return firstValueFrom(
      this.http.post<LearningSessionResponse>(
        `${this.apiBaseUrl}/sessions/${sessionId}/evaluation`,
        payload,
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

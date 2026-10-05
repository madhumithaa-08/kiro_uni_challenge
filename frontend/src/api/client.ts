// Typed API client. Components never call fetch directly (steering: frontend).

export interface Solution {
  id: number;
  title: string;
  platform: string;
  problem_slug: string;
  topic: string;
  language: string;
  code: string;
  explanation: string;
  notes: string;
  time_complexity: string;
  space_complexity: string;
  file_path: string;
  created_at: string;
  updated_at: string;
}

export interface TopicCount {
  topic: string;
  count: number;
}

export interface Progress {
  current_streak: number;
  longest_streak: number;
  total_solved: number;
  total_flashcards: number;
  by_topic: TopicCount[];
}

export interface Flashcard {
  id: number;
  problem_id: number;
  problem_title: string;
  front: string;
  back: string;
  due_date: string;
}

export interface SolutionCreate {
  title: string;
  code: string;
  topic: string;
  platform?: string;
  language?: string | null;
  problem_slug?: string | null;
  notes?: string;
}

export interface Recommendation {
  topic: string;
  recommended_topics: string[];
  note: string;
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
    } catch {
      /* keep statusText */
    }
    throw new ApiError(res.status, detail);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export const api = {
  health: () => request<{ status: string }>("/health"),

  listSolutions: (search?: string, topic?: string) => {
    const q = new URLSearchParams();
    if (search) q.set("search", search);
    if (topic) q.set("topic", topic);
    const qs = q.toString();
    return request<Solution[]>(`/solutions${qs ? `?${qs}` : ""}`);
  },
  getSolution: (id: number) => request<Solution>(`/solutions/${id}`),
  createSolution: (payload: SolutionCreate) =>
    request<Solution>("/solutions", { method: "POST", body: JSON.stringify(payload) }),
  updateSolution: (id: number, fields: { explanation?: string; notes?: string }) =>
    request<Solution>(`/solutions/${id}`, { method: "PATCH", body: JSON.stringify(fields) }),

  progress: () => request<Progress>("/progress"),

  dueCards: () => request<Flashcard[]>("/review/due"),
  gradeCard: (id: number, grade: "again" | "good" | "easy") =>
    request<{ id: number; due_date: string }>(`/review/${id}/grade`, {
      method: "POST",
      body: JSON.stringify({ grade }),
    }),

  topics: () => request<string[]>("/learn/topics"),
  path: (topic: string) =>
    request<{ topic: string; path: string[] }>(`/learn/path?topic=${encodeURIComponent(topic)}`),
  recommend: (topic: string) =>
    request<Recommendation>(`/learn/recommend?topic=${encodeURIComponent(topic)}`),
};

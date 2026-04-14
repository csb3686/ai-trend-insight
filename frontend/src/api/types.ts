/**
 * Backend API와 통신을 위한 공통 인터페이스 정의
 */

// --- Trends (트렌드) ---

export interface TrendHeatmapItem {
  tech_id: number;
  name: string;
  category: string;
  mention_count: number;
  rank: number;
  change_rate: number | null;
}

export interface TrendHeatmapResponse {
  year: number;
  month: number;
  data: TrendHeatmapItem[];
}

export interface TrendTopItem {
  name: string;
  category: string;
  change_rate: number;
  rank: number;
}

export interface TrendTop5Response {
  rising: TrendTopItem[];
  falling: TrendTopItem[];
}

export interface TrendTimelineItem {
  year: number;
  month: number;
  mention_count: number;
  rank: number;
}

export interface TrendTimelineResponse {
  tech_id: number;
  name: string;
  timeline: TrendTimelineItem[];
}

/** 대시보드 상단 요약 데이터 타입 */
export interface DashboardStatsResponse {
  news_count: number;
  github_count: number;
  tech_count: number;
  last_updated: string;
  updated_minutes_ago: number;
}

// --- Articles (기사) ---

export interface SourceInfo {
  id: number;
  name: string;
  url: string;
}

export interface ArticleListItem {
  id: number;
  title: string;
  url: string;
  source_name: string;
  type: 'news' | 'github_repo';
  published_at: string | null;
  created_at: string;
}

export interface ArticleListResponse {
  total: number;
  items: ArticleListItem[];
}

export interface ArticleDetail {
  id: number;
  title: string;
  url: string;
  content: string | null;
  description: string | null;
  author: string | null;
  type: string;
  source: SourceInfo;
  published_at: string | null;
  github_stars?: number;
  github_language?: string;
  technologies: string[];
}

// --- Chat (채팅) ---

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  answer: string;
  context?: string | null;
}

export interface HealthCheckResponse {
  status: string;
  database: string;
  timestamp: string;
  gemini_models?: string[];
}

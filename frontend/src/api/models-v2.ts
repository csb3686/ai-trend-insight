export type TrendHeatmapItem = {
  tech_id: number;
  name: string;
  category: string;
  mention_count: number;
  rank: number;
  change_rate: number | null;
};

export type TrendHeatmapResponse = {
  year: number;
  month: number;
  data: TrendHeatmapItem[];
};

export type TrendTopItem = {
  name: string;
  category: string;
  change_rate: number;
  rank: number;
};

export type TrendTop5Response = {
  rising: TrendTopItem[];
  falling: TrendTopItem[];
};

export type TrendTimelineItem = {
  year: number;
  month: number;
  mention_count: number;
  rank: number;
};

export type TrendTimelineResponse = {
  tech_id: number;
  name: string;
  timeline: TrendTimelineItem[];
};

export type DashboardStatsResponse = {
  news_count: number;
  github_count: number;
  tech_count: number;
  last_updated: string;
  updated_minutes_ago: number;
};

export type SourceInfo = {
  id: number;
  name: string;
  url: string;
};

export type ArticleListItem = {
  id: number;
  title: string;
  url: string;
  source_name: string;
  type: 'news' | 'github_repo';
  published_at: string | null;
  created_at: string;
};

export type ArticleListResponse = {
  total: number;
  items: ArticleListItem[];
};

export type ArticleDetail = {
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
};

export type ChatRequest = {
  message: string;
};

export type ChatResponse = {
  answer: string;
  context?: string | null;
};

export type HealthCheckResponse = {
  status: string;
  database: string;
  timestamp: string;
  gemini_models?: string[];
};

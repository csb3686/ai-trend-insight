import { useQuery } from '@tanstack/react-query';
import client from '../client';
import type { TrendTimelineResponse, ArticleListItem } from '../models-v2';

/**
 * 특정 기술의 상세 정보(타임라인, 설명) 및 연관 뉴스를 가져오는 통합 훅
 */
export const useTechDetail = (techId: number | null) => {
  // 1. 기술 시계열 추이 및 설명 조회
  const infoQuery = useQuery<TrendTimelineResponse>({
    queryKey: ['trends', 'timeline', techId],
    queryFn: async () => {
      if (!techId) throw new Error('Tech ID is required');
      const { data } = await client.get(`/trends/timeline/${techId}`);
      return data;
    },
    enabled: !!techId,
    staleTime: 1000 * 60 * 10, // 10분간 유지
  });

  // 2. 해당 기술 관련 뉴스 상위 3개 조회
  const articlesQuery = useQuery<ArticleListItem[]>({
    queryKey: ['articles', 'tech', techId],
    queryFn: async () => {
      if (!techId) throw new Error('Tech ID is required');
      const { data } = await client.get(`/articles/tech/${techId}`, {
        params: { limit: 3 }
      });
      return data;
    },
    enabled: !!techId,
    staleTime: 1000 * 60 * 5, // 5분간 유지
  });

  return {
    info: infoQuery.data,
    articles: articlesQuery.data,
    isLoading: infoQuery.isLoading || articlesQuery.isLoading,
    isError: infoQuery.isError || articlesQuery.isError,
    refetch: () => {
      infoQuery.refetch();
      articlesQuery.refetch();
    }
  };
};

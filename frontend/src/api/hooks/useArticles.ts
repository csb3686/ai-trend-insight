import { useQuery } from '@tanstack/react-query';
import client from '../client';
import type { ArticleListResponse } from '../models-v2';

/**
 * 기사 목록(뉴스 및 GitHub 저장소)을 가져오는 훅
 */
export const useArticles = (skip = 0, limit = 10, type?: string, q?: string, category?: string) => {
  return useQuery<ArticleListResponse>({
    queryKey: ['articles', skip, limit, type, q, category],
    queryFn: async () => {
      const { data } = await client.get('/articles', {
        params: { skip, limit, type, q, category },
      });
      return data;
    },
    staleTime: 1000 * 60 * 1, // 검색 반영을 위해 캐시 시간 1분으로 조정
  });
};

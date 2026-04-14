import { useQuery } from '@tanstack/react-query';
import client from '../client';
import type { ArticleListResponse } from '../models-v2';

/**
 * 기사 목록(뉴스 및 GitHub 저장소)을 가져오는 훅
 */
export const useArticles = (page = 1, pageSize = 10, type?: string) => {
  return useQuery<ArticleListResponse>({
    queryKey: ['articles', page, pageSize, type],
    queryFn: async () => {
      const { data } = await client.get('/articles', {
        params: { page, page_size: pageSize, type },
      });
      return data;
    },
    staleTime: 1000 * 60 * 3, // 3분간 캐시 유지
  });
};

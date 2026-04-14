import { useQuery } from '@tanstack/react-query';
import client from '../client';
import type { TrendHeatmapResponse, TrendTop5Response, DashboardStatsResponse } from '../models-v2';

/**
 * 대시보드 요약 상세 데이터를 가져오는 훅
 */
export const useDashboardSummary = () => {
  return useQuery<DashboardStatsResponse>({
    queryKey: ['trends', 'summary'],
    queryFn: async () => {
      const { data } = await client.get('/trends/summary');
      return data;
    },
    staleTime: 1000 * 60 * 5, // 5분간 유지
  });
};

/**
 * 기술 히트맵 데이터를 가져오는 훅
 */
export const useTrendHeatmap = (year?: number, month?: number) => {
  return useQuery<TrendHeatmapResponse>({
    queryKey: ['trends', 'heatmap', year, month],
    queryFn: async () => {
      const { data } = await client.get('/trends/heatmap', {
        params: { year, month },
      });
      return data;
    },
    staleTime: 1000 * 60 * 5, // 5분간 신선도 유지
  });
};

/**
 * 상승/하락 Top 5 트렌드 데이터를 가져오는 훅
 */
export const useTopTrends = () => {
  return useQuery<TrendTop5Response>({
    queryKey: ['trends', 'top5'],
    queryFn: async () => {
      const { data } = await client.get('/trends/top5');
      return data;
    },
    staleTime: 1000 * 60 * 10, // 10분간 유지
  });
};

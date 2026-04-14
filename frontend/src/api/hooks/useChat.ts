import { useMutation } from '@tanstack/react-query';
import client from '../client';
import type { ChatRequest, ChatResponse } from '../models-v2';

/**
 * AI 챗봇에게 질문을 보내고 답변을 받는 훅
 */
export const useChatMutation = () => {
  return useMutation<ChatResponse, Error, ChatRequest>({
    mutationFn: async (payload: ChatRequest) => {
      const { data } = await client.post('/chat', payload);
      return data;
    },
  });
};

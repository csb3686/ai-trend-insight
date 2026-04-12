export const dashboardStats = {
  newsCount: 12847,
  newsAddedToday: 324,
  githubRepos: 3291,
  githubAddedToday: 58,
  analyzedTechs: 487,
  techsAddedThisWeek: 12,
  lastUpdated: '1,043',
  updatedMinutesAgo: 2,
};

export const techHeatmapData = [
  { id: 'gpt-5', name: 'GPT-5', mentions: 2847, category: 'AI/ML' },
  { id: 'langchain', name: 'LangChain', mentions: 2108, category: 'AI/ML' },
  { id: 'react-19', name: 'React 19', mentions: 1956, category: 'Frontend' },
  { id: 'kubernetes', name: 'Kubernetes', mentions: 1742, category: 'DevOps' },
  { id: 'rag', name: 'RAG', mentions: 1689, category: 'AI/ML' },
  { id: 'rust', name: 'Rust', mentions: 1534, category: 'Backend' },
  { id: 'nextjs-15', name: 'Next.js 15', mentions: 1421, category: 'Frontend' },
  { id: 'docker', name: 'Docker', mentions: 1387, category: 'DevOps' },
  { id: 'llama-4', name: 'Llama 4', mentions: 1298, category: 'AI/ML' },
  { id: 'apache-kafka', name: 'Apache Kafka', mentions: 1156, category: 'Data' },
];

export const topTrendsData = [
  { id: 1, name: 'Agentic AI', category: 'AI/ML', desc: '자율적 AI 에이전트 프레임워크의 급격한 성장', changePercent: 142, isUp: true },
  { id: 2, name: 'React Server Components', category: 'Frontend', desc: '서버 컴포넌트 패턴 채택 가속화', changePercent: 87, isUp: true },
  { id: 3, name: 'Rust for WebAssembly', category: 'Backend', desc: 'WASM 기반 고성능 웹 앱 증가', changePercent: 63, isUp: true },
  { id: 4, name: 'GitOps', category: 'DevOps', desc: '성숙기 진입, 신규 언급 감소', changePercent: -12, isUp: false },
  { id: 5, name: 'Vector Databases', category: 'Data', desc: 'RAG 파이프라인 핵심 인프라로 자리잡기', changePercent: 95, isUp: true },
];

export const latestNewsData = [
  { id: 1, title: 'OpenAI, GPT-5 멀티모달 성능 벤치마크 공개', category: 'AI/ML', source: 'TechCrunch', timeAgo: '12분 전', url: '#' },
  { id: 2, title: 'React 19 RC2 릴리즈 - 서버 액션 안정화', category: 'Frontend', source: 'React Blog', timeAgo: '34분 전', url: '#' },
  { id: 3, title: 'Kubernetes 1.32 보안 패치 긴급 배포', category: 'DevOps', source: 'CNCF', timeAgo: '1시간 전', url: '#' },
  { id: 4, title: 'Google DeepMind, 새로운 코드 생성 AI \'AlphaCode 3\' 발표', category: 'AI/ML', source: 'Google AI Blog', timeAgo: '2시간 전', url: '#' },
  { id: 5, title: 'Vercel, Edge Runtime 성능 2배 향상 업데이트', category: 'Frontend', source: 'Vercel Blog', timeAgo: '3시간 전', url: '#' },
];

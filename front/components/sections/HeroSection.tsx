// components/sections/HeroSection.tsx
import { Button } from "@/components/ui/button";

export function HeroSection() {
  return (
    <section className="container flex flex-col items-center justify-center text-center py-24 sm:py-32">
      <h1 className="text-4xl font-bold tracking-tight sm:text-6xl max-w-3xl">
        IPTV PPL 광고 효과, 분석 및 리포팅 플랫폼
      </h1>
      <p className="mt-6 text-lg leading-8 text-muted-foreground max-w-2xl">
        AI 기반 실시간 분석으로 IPTV 광고의 성과를 정확하게 측정하고, 데이터 기반 인사이트로 ROI를 극대화하세요.
      </p>
      <div className="mt-10">
        <Button size="lg">분석 시작하기 →</Button>
      </div>
    </section>
  );
}
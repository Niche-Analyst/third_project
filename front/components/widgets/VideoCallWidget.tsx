//front/components/widgets/VideoCallWidget.tsx
import Image from "next/image";
// 비디오콜 위젯 UI를 위한 독립적인 컴포넌트
export function VideoCallWidget() {
  return (
    <div className="relative w-full max-w-sm">
      {/* 상단 노란색 텍스트 박스 */}
      <div className="absolute -top-8 left-1/2 z-10 -translate-x-1/2 transform rounded-2xl bg-accent p-4 shadow-lg">
        <p className="whitespace-nowrap text-center font-bold text-accent-foreground">
          Ons pensioen<br />en plan
        </p>
      </div>

      {/* 메인 이미지 카드 */}
      <div className="overflow-hidden rounded-3xl border bg-card shadow-xl">
        <Image
          src="https://placehold.co/400x400/2d3748/ffffff?text=Max+Lee"
          alt="Max Lee, Gecertificeerd Financieel Planner"
          width={400}
          height={400}
          className="h-auto w-full"
          priority // 히어로 섹션의 주요 이미지이므로 우선적으로 로드합니다.
        />
        <div className="p-4 text-center">
          <p className="font-bold">Max Lee</p>
          <p className="text-sm text-muted-foreground">Gecertificeerd Financieel...</p>
        </div>
      </div>
    </div>
  );
}

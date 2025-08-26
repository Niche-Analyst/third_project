import { HeroSection } from "@/components/sections/HeroSection";
import { FeatureSection } from "@/components/sections/FeatureSection";
import { HowItWorksSection } from "@/components/sections/HowItWorksSection";
import { CtaSection } from "@/components/sections/CtaSection";

export default function Home() {
  return (
    <div className="flex flex-col">{/* items-center 제거 */}
      <HeroSection />
      <FeatureSection />
      <HowItWorksSection />
      <CtaSection />
    </div>
  );
}

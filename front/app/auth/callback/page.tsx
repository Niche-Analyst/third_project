'use client'; 

import NavBar from "@/components/common/NavBar";
import { HeroSection } from "@/components/sections/HeroSection";
import { FeatureSection } from "@/components/sections/FeatureSection";
import { HowItWorksSection } from "@/components/sections/HowItWorksSection";
import { CtaSection } from "@/components/sections/CtaSection";

export default function Home() {
  return (
    <div className="flex flex-col">
      <NavBar />
      <HeroSection />
      <FeatureSection />
      <HowItWorksSection />
      <CtaSection />
    </div>
  );
}
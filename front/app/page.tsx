import NavBar from "../components/common/NavBar";
import { HeroSection } from "../components/sections/HeroSection";
import { FeatureSection } from "../components/sections/FeatureSection";
import { HowItWorksSection } from "../components/sections/HowItWorksSection";
import { CtaSection } from "../components/sections/CtaSection";

export default function HomePage() {
  return (
    <>
      <NavBar />
      <div className="flex flex-col items-center mt-16"> {/* NavBar 높이만큼 margin */}
        <section id="home"><HeroSection /></section>
        <section id="features"><FeatureSection /></section>
        <section id="howitworks"><HowItWorksSection /></section>
        <section id="pricing"><CtaSection /></section>
      </div>
    </>
  );
}

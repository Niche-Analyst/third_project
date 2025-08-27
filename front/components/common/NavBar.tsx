"use client";

import React from "react";
import { Link as ScrollLink } from "react-scroll";

const NavBar = () => {
  return (
    <nav className="fixed top-0 w-full bg-transparent text-black h-16 flex items-center justify-center px-10 shadow-lg border-b border-gray-300/50 z-50">
      <div className="flex w-full items-center justify-center space-x-16">
    
        <ul className="flex gap-16 list-none m-0 p-0 items-center">

          <li className="relative font-semibold cursor-pointer group hover:text-orange-600 transition-colors">
            Product ▼
            <ul className="absolute top-full left-1/2 transform -translate-x-1/2 bg-white rounded-md shadow-xl mt-2 opacity-0 group-hover:opacity-100 group-hover:scale-105 transition-all w-48 text-black">
              <li className="px-4 py-2 hover:bg-gray-100"><ScrollLink to="features" smooth duration={500}>Features</ScrollLink></li>
              <li className="px-4 py-2 hover:bg-gray-100"><ScrollLink to="howitworks" smooth duration={500}>How It Works</ScrollLink></li>
              <li className="px-4 py-2 hover:bg-gray-100"><ScrollLink to="pricing" smooth duration={500}>Pricing</ScrollLink></li>
              <li className="px-4 py-2 hover:bg-gray-100"><ScrollLink to="integrations" smooth duration={500}>Integrations</ScrollLink></li>
              <li className="px-4 py-2 hover:bg-gray-100"><ScrollLink to="demo" smooth duration={500}>Demo</ScrollLink></li>
              <li className="px-4 py-2 hover:bg-gray-100"><ScrollLink to="roadmap" smooth duration={500}>Roadmap</ScrollLink></li>
            </ul>
          </li>

          <li className="relative font-semibold cursor-pointer group hover:text-orange-600 transition-colors">
            Why Us ▼
            <ul className="absolute top-full left-1/2 transform -translate-x-1/2 bg-white rounded-md shadow-xl mt-2 opacity-0 group-hover:opacity-100 group-hover:scale-105 transition-all w-48 text-black">
              <li className="px-4 py-2 hover:bg-gray-100"><ScrollLink to="team" smooth duration={500}>Team</ScrollLink></li>
              <li className="px-4 py-2 hover:bg-gray-100"><ScrollLink to="mission" smooth duration={500}>Mission</ScrollLink></li>
              <li className="px-4 py-2 hover:bg-gray-100"><ScrollLink to="ourpromise" smooth duration={500}>Our Promise</ScrollLink></li>
              <li className="px-4 py-2 hover:bg-gray-100"><ScrollLink to="values" smooth duration={500}>Values</ScrollLink></li>
            </ul>
          </li>
          <li className="font-semibold cursor-pointer hover:text-orange-600 transition-colors">
            <ScrollLink to="contact" smooth duration={500}>Contact</ScrollLink>
          </li>
        </ul>

        <button
          className="px-5 py-2 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 hover:scale-105 hover:shadow-md transition-transform cursor-pointer"
        >
          Get Started
        </button>
      </div>
    </nav>
  );
};

export default NavBar;
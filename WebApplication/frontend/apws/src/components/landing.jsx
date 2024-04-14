import React, { useState, useEffect } from "react";
import { Navigation } from "./LandingPage/navigation";
import { Header } from "./LandingPage/header";
import { Features } from "./LandingPage/features";
import { About } from "./LandingPage/about";
import { Services } from "./LandingPage/services";
import { Gallery } from "./LandingPage/gallery";
import { Testimonials } from "./LandingPage/testimonials";
import { Team } from "./LandingPage/Team";
// import { Contact } from "./LandingPage/contact";
import JsonData from "./LandingPage/data.json";
import SmoothScroll from "smooth-scroll";
import "../styles/landing.css";

export const scroll = new SmoothScroll('a[href*="#"]', {
  speed: 1000,
  speedAsDuration: true,
});

const Landing = () => {
  const [landingPageData, setLandingPageData] = useState({});
  useEffect(() => {
    setLandingPageData(JsonData);
  }, []);

  return (
    <div>
      <Navigation />
      <Header data={landingPageData.Header} />
      {/* <Features data={landingPageData.Features} /> */}
      <About data={landingPageData.About} />
      <Services data={landingPageData.Services} />
      <Gallery data={landingPageData.Gallery} />
      <Features data={landingPageData.Features} />
      {/* <Testimonials data={landingPageData.Testimonials} /> */}
      <Team data={landingPageData.Team} />
      {/* <Contact data={landingPageData.Contact} /> */}
    </div>
  );
};

export default Landing;
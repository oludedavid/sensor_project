import { useEffect, useState } from "react";

export default function useScreenSize() {
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const [windowHeight, setWindowHeight] = useState(window.innerHeight);
  const [isMobile, setIsMobile] = useState(false);
  const [isTablet, setIsTablet] = useState(false);
  const [isDesktop, setIsDesktop] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      const height = window.innerHeight;

      setWindowWidth(width);
      setWindowHeight(height);

      // Tailwind-style breakpoints
      if (width < 768) {
        setIsMobile(true);
        setIsTablet(false);
        setIsDesktop(false);
      } else if (width >= 768 && width < 1024) {
        setIsMobile(false);
        setIsTablet(true);
        setIsDesktop(false);
      } else {
        setIsMobile(false);
        setIsTablet(false);
        setIsDesktop(true);
      }
    };

    handleResize();

    window.addEventListener("resize", handleResize);
    return () => {
      console.log("Cleanup: removing resize event listener");
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return {
    windowWidth,
    windowHeight,
    isMobile,
    isTablet,
    isDesktop,
  };
}

import { useEffect, useState } from "react";
import Image from "next/image";
import classNames from "classnames";

type TImage = {
  imageUrl: string;
  alt: string;
};

const imagesData: TImage[] = [
  { imageUrl: "/images/pic1.jpg", alt: "Registration pic1" },
  { imageUrl: "/images/pic2.jpg", alt: "Registration pic2" },
  { imageUrl: "/images/pic3.jpeg", alt: "Registration pic3" },
  { imageUrl: "/images/pic4.jpeg", alt: "Registration pic4" },
  { imageUrl: "/images/pic5.jpeg", alt: "Registration pic5" },
];

export default function ImageTransition({ className }: { className?: string }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [prevIndex, setPrevIndex] = useState(0);
  const [isFading, setIsFading] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setIsFading(true);
      setPrevIndex(currentIndex);
      setTimeout(() => {
        setCurrentIndex((prev) => (prev + 1) % imagesData.length);
        setIsFading(false);
      }, 500);
    }, 4000);

    return () => clearInterval(interval);
  }, [currentIndex]);

  return (
    <div className={`w-full h-full relative overflow-hidden ${className}`}>
      {/* Previous Image */}
      <Image
        key={currentIndex}
        src={imagesData[prevIndex].imageUrl}
        alt={imagesData[prevIndex].alt}
        fill
        className={classNames(
          "object-cover absolute top-0 left-0 w-full h-full transition-opacity duration-500 ease-in-out",
          { "opacity-0": !isFading, "opacity-100": isFading }
        )}
      />
      {/* Current Image */}
      <Image
        key={currentIndex + 1}
        src={imagesData[currentIndex].imageUrl}
        alt={imagesData[currentIndex].alt}
        fill
        className={classNames(
          "object-cover absolute top-0 left-0 w-full h-full transition-opacity duration-500 ease-in-out",
          { "opacity-100": !isFading, "opacity-0": isFading }
        )}
      />
    </div>
  );
}

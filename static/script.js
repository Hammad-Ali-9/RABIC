
const track = document.querySelector('.carousel-track');
const slides = Array.from(track.children);
const slideWidth = slides[0].getBoundingClientRect().width;

let currentIndex = 1; // Start from the first real slide

// Function to move the track
function moveToSlide(index) {
  track.style.transition = "transform 0.5s ease-in-out";
  track.style.transform = `translateX(-${index * slideWidth}px)`;

  currentIndex = index;

  // Handle looping logic
  track.addEventListener(
    "transitionend",
    () => {
      if (currentIndex === 0) {
        // If at the duplicate last slide, jump to the real last slide
        track.style.transition = "none";
        track.style.transform = `translateX(-${(slides.length - 2) * slideWidth}px)`;
        currentIndex = slides.length - 2;
      } else if (currentIndex === slides.length - 1) {
        // If at the duplicate first slide, jump to the real first slide
        track.style.transition = "none";
        track.style.transform = `translateX(-${slideWidth}px)`;
        currentIndex = 1;
      }
    },
    { once: true } // Ensure this only runs once per transition
  );
}

// Auto-slide every 2 seconds
setInterval(() => {
  moveToSlide(currentIndex + 1);
}, 2000);


const track1 = document.querySelector('.carousel-track1');
const slides1 = Array.from(track1.children);
const slideWidth1 = slides1[0].getBoundingClientRect().width;

let currentIndex1 = 1; // Start from the first real slide

// Function to move the track
function moveToSlide(index) {
  track1.style.transition = "transform 0.5s ease-in-out";
  track1.style.transform = `translateX(+${index * slideWidth1}px)`;

  currentIndex1 = index;

  // Handle looping logic
  track1.addEventListener(
    "transitionend",
    () => {
      if (currentIndex1 === 0) {
        // If at the duplicate last slide, jump to the real last slide
        track1.style.transition = "none";
        track1.style.transform = `translateX(${(slides1.length + 2) * slideWidth1}px)`;
        currentIndex1 = slides1.length + 2;
      } else if (currentIndex1 === slides1.length + 1) {
        // If at the duplicate first slide, jump to the real first slide
        track1.style.transition = "none";
        track1.style.transform = `translateX(+${slideWidth1}px)`;
        currentIndex1 = 1;
      }
    },
    { once: true } // Ensure this only runs once per transition
  );
}

// Auto-slide every 2 seconds
setInterval(() => {
  moveToSlide(currentIndex1 - 1);
}, 2000);

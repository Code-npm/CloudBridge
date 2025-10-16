
const facts = document.getElementById('facts');
let scrollSpeed = 1; // 🔹 change this value to control speed (1–5 recommended)

function autoScroll() {
  facts.scrollLeft += scrollSpeed;
  // when it reaches end, go back to start
  if (facts.scrollLeft + facts.clientWidth >= facts.scrollWidth) {
    facts.scrollLeft = 0;
  }
}

// run autoScroll repeatedly
setInterval(autoScroll, 20); // smaller interval = smoother motion


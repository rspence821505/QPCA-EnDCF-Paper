// Render KaTeX math in all slides
// Called after Reveal.js has parsed markdown into DOM
function renderAllMath() {
  var container = document.querySelector('.reveal .slides');
  if (!container) return;

  // Check if there's still raw $$ in the DOM (unrendered math)
  if (container.innerHTML.indexOf('$$') === -1 &&
      container.innerHTML.indexOf('\\mathbf') === -1) {
    return; // already rendered or no math
  }

  renderMathInElement(container, {
    delimiters: [
      {left: "$$", right: "$$", display: true},
      {left: "$", right: "$", display: false}
    ],
    throwOnError: false,
    trust: true,
    macros: {
      "\\R": "\\mathbb{R}",
      "\\E": "\\mathbb{E}"
    }
  });
  console.log('KaTeX: math rendered');
}

// The problem: reveal-md scripts load AFTER Reveal.initialize(),
// but the markdown plugin may still be parsing slides.
// Solution: listen to 'ready' if not ready yet, otherwise just render.
if (typeof Reveal !== 'undefined') {
  if (Reveal.isReady()) {
    // Reveal already ready, render now
    renderAllMath();
  } else {
    // Wait for ready
    Reveal.on('ready', function() {
      renderAllMath();
    });
  }
  // Also re-render on slide change (for lazy-loaded content)
  Reveal.on('slidechanged', function() {
    renderAllMath();
  });
} else {
  // Reveal not defined yet, wait
  window.addEventListener('load', function() {
    setTimeout(renderAllMath, 500);
    if (typeof Reveal !== 'undefined') {
      Reveal.on('slidechanged', function() { renderAllMath(); });
    }
  });
}

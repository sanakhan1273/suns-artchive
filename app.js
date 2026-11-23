const works = window.WORKS || { graphics: [], motion: [] };
const tabs = document.querySelectorAll(".tab");
const panels = { graphics: document.getElementById("graphics"), motion: document.getElementById("motion") };
const lightbox = document.getElementById("lightbox");

// Videos only play while on screen, so a big wall of them stays smooth.
const videoWatcher = new IntersectionObserver((entries) => {
  entries.forEach(({ target, isIntersecting }) => {
    if (isIntersecting) target.play().catch(() => {});
    else target.pause();
  });
}, { rootMargin: "200px" });

function makeVideo(src) {
  const v = document.createElement("video");
  v.src = src;
  v.muted = true;
  v.loop = true;
  v.playsInline = true;
  v.preload = "metadata";
  return v;
}

function fill(kind) {
  const panel = panels[kind];
  const files = works[kind] || [];
  if (!files.length) {
    panel.innerHTML = `<p class="empty">Nothing here yet.<br>Drop files into <code>${kind}/</code> and run <code>python3 update.py</code>.</p>`;
    return;
  }
  files.forEach((src) => {
    const tile = document.createElement("div");
    tile.className = "tile";
    let media;
    if (kind === "motion") {
      media = makeVideo(src);
      videoWatcher.observe(media);
    } else {
      media = document.createElement("img");
      media.src = src;
      media.loading = "lazy";
      media.alt = "";
    }
    tile.appendChild(media);
    tile.addEventListener("click", () => openLightbox(kind, src));
    panel.appendChild(tile);
  });
}

function openLightbox(kind, src) {
  lightbox.innerHTML = "";
  let media;
  if (kind === "motion") {
    media = makeVideo(src);
    media.controls = true;
    media.autoplay = true;
  } else {
    media = document.createElement("img");
    media.src = src;
  }
  lightbox.appendChild(media);
  lightbox.hidden = false;
}

function closeLightbox() {
  lightbox.hidden = true;
  lightbox.innerHTML = "";
}
lightbox.addEventListener("click", (e) => { if (e.target === lightbox) closeLightbox(); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeLightbox(); });

function show(kind) {
  tabs.forEach((t) => t.classList.toggle("is-active", t.dataset.tab === kind));
  Object.entries(panels).forEach(([k, p]) => (p.hidden = k !== kind));
  if (location.hash !== "#" + kind) history.replaceState(null, "", "#" + kind);
}

tabs.forEach((t) => t.addEventListener("click", () => show(t.dataset.tab)));

fill("graphics");
fill("motion");
show(location.hash === "#motion" ? "motion" : "graphics");

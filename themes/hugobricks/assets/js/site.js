(() => {
  const body = document.body;
  const header = document.querySelector("[data-header]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const nav = document.getElementById("site-nav");
  const subToggles = [...document.querySelectorAll("[data-sub-toggle]")];
  const wide = window.matchMedia("(min-width: 80em)");

  const closeSubs = (except) => {
    subToggles.forEach((t) => {
      if (t !== except) t.setAttribute("aria-expanded", "false");
    });
  };

  const setMenu = (open) => {
    if (!menuToggle) return;
    menuToggle.setAttribute("aria-expanded", String(open));
    body.classList.toggle("menu-open", open);
    if (open) {
      const first = nav && nav.querySelector("a, button");
      if (first) first.focus();
    }
  };

  if (menuToggle) {
    menuToggle.addEventListener("click", () => {
      setMenu(menuToggle.getAttribute("aria-expanded") !== "true");
    });
  }

  subToggles.forEach((t) => {
    t.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = t.getAttribute("aria-expanded") !== "true";
      closeSubs(t);
      t.setAttribute("aria-expanded", String(open));
    });
  });

  document.addEventListener("click", (e) => {
    if (!e.target.closest(".nav__item--sub")) closeSubs();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    const openSub = subToggles.find((t) => t.getAttribute("aria-expanded") === "true");
    if (openSub) {
      closeSubs();
      openSub.focus();
    } else if (body.classList.contains("menu-open")) {
      setMenu(false);
      menuToggle.focus();
    }
  });

  if (nav) {
    nav.addEventListener("focusout", (e) => {
      const sub = e.target.closest(".nav__item--sub");
      if (sub && !sub.contains(e.relatedTarget)) closeSubs();
    });
  }

  wide.addEventListener("change", () => {
    setMenu(false);
    closeSubs();
  });

  const sentinel = document.getElementById("top-sentinel");
  if (header && sentinel && "IntersectionObserver" in window) {
    const offset = header.classList.contains("site-header--over") ? 80 : 8;
    sentinel.style.height = offset + "px";
    new IntersectionObserver(([entry]) => {
      header.classList.toggle("is-scrolled", !entry.isIntersecting);
    }).observe(sentinel);
  }
})();

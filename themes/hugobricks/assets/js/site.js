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

  const calm = window.matchMedia("(prefers-reduced-motion: reduce)");
  document.querySelectorAll("[data-tour]").forEach((root) => {
    const track = root.querySelector(".tour__track");
    const tabList = root.querySelector("[data-tour-tabs]");
    if (!track || !tabList) return;
    const slides = [...track.children];
    const tabs = [...tabList.querySelectorAll("button")];
    let active = 0;
    let ticking = false;

    const mark = (i) => {
      if (i === active) return;
      active = i;
      tabs.forEach((t, n) => {
        if (n === i) t.setAttribute("aria-current", "true");
        else t.removeAttribute("aria-current");
      });
    };

    let target = -1;
    let release = 0;
    const show = (i) => {
      target = i;
      clearTimeout(release);
      release = setTimeout(() => { target = -1; }, 900);
      track.scrollTo({ left: slides[i].offsetLeft, behavior: calm.matches ? "auto" : "smooth" });
      mark(i);
    };

    tabs.forEach((t, i) => t.addEventListener("click", () => show(i)));

    tabList.addEventListener("keydown", (e) => {
      const dir = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
      const from = tabs.indexOf(document.activeElement);
      if (!dir || from < 0) return;
      e.preventDefault();
      const to = (from + dir + tabs.length) % tabs.length;
      tabs[to].focus();
      show(to);
    });

    track.addEventListener("scroll", () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        ticking = false;
        const step = slides[1] ? slides[1].offsetLeft - slides[0].offsetLeft : track.clientWidth;
        const i = Math.min(slides.length - 1, Math.max(0, Math.round(track.scrollLeft / step)));
        if (target >= 0) {
          if (i !== target) return;
          target = -1;
        }
        mark(i);
      });
    }, { passive: true });

    tabList.hidden = false;
  });

  document.querySelectorAll("[data-tabs]").forEach((root) => {
    const list = root.querySelector("[role=tablist]");
    if (!list) return;
    const tabs = [...list.querySelectorAll("[role=tab]")];
    const panels = tabs.map((t) => document.getElementById(t.getAttribute("aria-controls")));

    const select = (i, focus) => {
      tabs.forEach((t, n) => {
        const on = n === i;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        panels[n].hidden = !on;
      });
      if (focus) tabs[i].focus();
    };

    tabs.forEach((t, i) => t.addEventListener("click", () => select(i)));

    list.addEventListener("keydown", (e) => {
      const from = tabs.indexOf(document.activeElement);
      if (from < 0) return;
      const to = { ArrowRight: from + 1, ArrowLeft: from - 1, Home: 0, End: tabs.length - 1 }[e.key];
      if (to === undefined) return;
      e.preventDefault();
      select((to + tabs.length) % tabs.length, true);
    });

    const fromHash = () => {
      let target = null;
      try { target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch { target = null; }
      const i = target ? panels.findIndex((p) => p.contains(target)) : -1;
      if (i < 0) return false;
      select(i);
      target.scrollIntoView();
      return true;
    };

    panels.forEach((p) => p.setAttribute("role", "tabpanel"));
    root.classList.add("is-tabbed");
    list.hidden = false;
    if (!fromHash()) select(0);
    window.addEventListener("hashchange", fromHash);
  });

  const mores = [...document.querySelectorAll(".person__more")];
  if (mores.length) {
    const fit = () => {
      mores.forEach((btn) => {
        const words = document.getElementById(btn.getAttribute("aria-controls"));
        if (!words || words.classList.contains("is-open")) return;
        btn.hidden = words.scrollHeight <= words.clientHeight + 1;
      });
    };
    mores.forEach((btn) => {
      btn.addEventListener("click", () => {
        const words = document.getElementById(btn.getAttribute("aria-controls"));
        const open = btn.getAttribute("aria-expanded") !== "true";
        words.classList.toggle("is-open", open);
        btn.setAttribute("aria-expanded", String(open));
        btn.textContent = open ? btn.dataset.less : btn.dataset.more;
      });
    });
    fit();
    if ("ResizeObserver" in window) new ResizeObserver(fit).observe(document.querySelector(".people"));
    else window.addEventListener("resize", fit);
  }

  const callbar = document.querySelector(".callbar");
  if (callbar) {
    let ticking = false;
    const update = () => {
      ticking = false;
      body.classList.toggle("callbar-on", window.scrollY > 200);
    };
    window.addEventListener("scroll", () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    }, { passive: true });
    update();
  }
})();

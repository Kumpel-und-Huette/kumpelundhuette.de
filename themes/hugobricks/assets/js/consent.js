import { gtm } from "@params";

const KEY = "kumpel-consent";
const VERSION = 1;
const MAX_AGE = 365 * 24 * 60 * 60 * 1000;

window.dataLayer = window.dataLayer || [];
// Consent commands only work when pushed as an Arguments object, not as an array.
function gtag() {
  window.dataLayer.push(arguments);
}

gtag("consent", "default", {
  ad_storage: "denied",
  ad_user_data: "denied",
  ad_personalization: "denied",
  analytics_storage: "denied",
  functionality_storage: "denied",
  personalization_storage: "denied",
});
gtag("set", "ads_data_redaction", true);

const read = () => {
  try {
    const c = JSON.parse(localStorage.getItem(KEY));
    return c && c.v === VERSION && Date.now() - c.t < MAX_AGE ? c : null;
  } catch {
    return null;
  }
};

let choice = read();
let loaded = false;

const grant = () => {
  gtag("consent", "update", { analytics_storage: "granted" });
  if (loaded || !gtm) return;
  loaded = true;
  window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
  const s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtm.js?id=" + encodeURIComponent(gtm);
  document.head.append(s);
};

const clearCookies = () => {
  const host = location.hostname.split(".");
  document.cookie.split("; ").forEach((c) => {
    const name = c.split("=")[0];
    if (!/^_(ga|gid|gat)/.test(name)) return;
    for (let i = 0; i < host.length - 1; i++) {
      document.cookie = name + "=; Max-Age=0; Path=/; Domain=" + host.slice(i).join(".");
    }
    document.cookie = name + "=; Max-Age=0; Path=/";
  });
};

if (choice && choice.analytics) grant();

document.addEventListener("DOMContentLoaded", () => {
  const banner = document.getElementById("consent");
  if (!banner) return;
  const root = document.documentElement;
  const title = document.getElementById("consent-title");
  const state = banner.querySelector("[data-consent-state]");
  let opener = null;

  const fit = () => {
    if (banner.hidden) return;
    const offset = parseFloat(getComputedStyle(banner).bottom) || 0;
    root.style.setProperty("--consent-h", Math.ceil(banner.offsetHeight + offset) + "px");
  };

  const show = () => {
    state.hidden = !choice;
    if (choice) state.textContent = choice.analytics ? state.dataset.accepted : state.dataset.rejected;
    banner.hidden = false;
    document.body.classList.add("consent-open");
    fit();
  };

  const hide = () => {
    banner.hidden = true;
    document.body.classList.remove("consent-open");
    root.style.removeProperty("--consent-h");
    if (opener) opener.focus();
    opener = null;
  };

  const decide = (analytics) => {
    choice = { v: VERSION, analytics, t: Date.now() };
    try {
      localStorage.setItem(KEY, JSON.stringify(choice));
    } catch {}
    if (analytics) {
      grant();
    } else {
      gtag("consent", "update", { analytics_storage: "denied" });
      clearCookies();
      // Tag Manager cannot be unloaded from a running page.
      if (loaded) {
        location.reload();
        return;
      }
    }
    hide();
  };

  banner.querySelectorAll("[data-consent]").forEach((b) => {
    b.addEventListener("click", () => decide(b.dataset.consent === "accept"));
  });
  document.querySelectorAll("[data-consent-open]").forEach((b) => {
    b.addEventListener("click", () => {
      opener = b;
      show();
      title.focus();
    });
  });
  banner.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && choice) hide();
  });
  if ("ResizeObserver" in window) new ResizeObserver(fit).observe(banner);

  if (!choice) show();
});

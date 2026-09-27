/**
 * NubeParaPymes — English Portal Interactive Controller
 * Provides zero-flicker client-side search, category filtering, dark mode,
 * and activity tracking for en/index.html without wiping pre-rendered DOM.
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", init);

  function init() {
    initTheme();
    initSearchAndFilters();
    initActivity();
    initFavorites();
    initVoiceSearch();
  }

  // --- THEME (DARK / LIGHT MODE) ---
  function initTheme() {
    var switchBtn = document.querySelector('header button[role="switch"]');
    var html = document.documentElement;

    function setTheme(isDark) {
      if (isDark) {
        html.classList.add("dark");
        if (switchBtn) {
          switchBtn.setAttribute("aria-checked", "true");
          var thumb = switchBtn.querySelector("span.z-10");
          if (thumb) {
            thumb.classList.remove("translate-x-0");
            thumb.classList.add("translate-x-7");
          }
        }
      } else {
        html.classList.remove("dark");
        if (switchBtn) {
          switchBtn.setAttribute("aria-checked", "false");
          var thumb = switchBtn.querySelector("span.z-10");
          if (thumb) {
            thumb.classList.remove("translate-x-7");
            thumb.classList.add("translate-x-0");
          }
        }
      }
    }

    var savedTheme = localStorage.getItem("theme");
    var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    var isDark = savedTheme ? savedTheme === "dark" : prefersDark;
    setTheme(isDark);

    if (switchBtn) {
      switchBtn.addEventListener("click", function () {
        var currentDark = html.classList.contains("dark");
        var nextDark = !currentDark;
        setTheme(nextDark);
        try {
          localStorage.setItem("theme", nextDark ? "dark" : "light");
        } catch (e) {}
      });
    }
  }

  // --- SEARCH AND CATEGORY FILTERS ---
  function initSearchAndFilters() {
    var searchInput = document.querySelector('header input[type="search"]');
    var tabList = document.querySelector('[role="tablist"]');
    var tabs = tabList ? Array.from(tabList.querySelectorAll('button[role="tab"]')) : [];
    var grid = document.querySelector("main .grid");
    if (!grid) return;

    var cards = Array.from(grid.children);
    var countDisplay = document.querySelector("main h2 + p");
    var activeCategory = "All";
    var activeQuery = "";

    var activeTabClass = "border-brand bg-brand text-white shadow-[0_8px_20px_-10px_rgba(59,130,246,0.8)]";
    var inactiveTabClass = "border-line bg-surface text-fg-muted hover:border-brand hover:text-brand";

    function filterTools() {
      var visibleCount = 0;
      var q = activeQuery.trim().toLowerCase();

      cards.forEach(function (card) {
        var categoryBadge = card.querySelector("span.text-brand");
        var catText = categoryBadge ? categoryBadge.textContent.trim() : "";
        var titleEl = card.querySelector("h3");
        var descEl = card.querySelector("p");
        var title = titleEl ? titleEl.textContent.toLowerCase() : "";
        var desc = descEl ? descEl.textContent.toLowerCase() : "";

        var matchesCat = (activeCategory === "All") || (catText.toLowerCase() === activeCategory.toLowerCase());
        var matchesQuery = !q || title.indexOf(q) !== -1 || desc.indexOf(q) !== -1;

        if (matchesCat && matchesQuery) {
          card.style.display = "";
          visibleCount++;
        } else {
          card.style.display = "none";
        }
      });

      if (countDisplay) {
        countDisplay.textContent = visibleCount + (visibleCount === 1 ? " result" : " results");
      }

      var emptyNotice = document.getElementById("np-en-no-results");
      if (visibleCount === 0) {
        if (!emptyNotice) {
          emptyNotice = document.createElement("div");
          emptyNotice.id = "np-en-no-results";
          emptyNotice.className = "col-span-full py-16 text-center text-fg-muted";
          emptyNotice.innerHTML = '<p class="text-lg font-semibold text-fg">No tools found for "' + escapeHtml(q) + '".</p><p class="mt-2 text-sm">Try searching with other keywords or clear your filter.</p>';
          grid.appendChild(emptyNotice);
        } else {
          emptyNotice.querySelector("p").textContent = 'No tools found for "' + q + '".';
          emptyNotice.style.display = "";
        }
      } else if (emptyNotice) {
        emptyNotice.style.display = "none";
      }
    }

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        tabs.forEach(function (t) {
          t.setAttribute("aria-selected", "false");
          t.className = t.className.replace(activeTabClass, "").trim() + " " + inactiveTabClass;
          var badge = t.querySelector("span");
          if (badge) {
            badge.className = "rounded-full px-1.5 text-xs bg-elevated text-fg-muted";
          }
        });

        tab.setAttribute("aria-selected", "true");
        tab.className = tab.className.replace(inactiveTabClass, "").trim() + " " + activeTabClass;
        var activeBadge = tab.querySelector("span");
        if (activeBadge) {
          activeBadge.className = "rounded-full px-1.5 text-xs bg-white/20 text-white";
        }

        // Get category name
        var rawText = tab.childNodes[tab.childNodes.length - 2] ? tab.childNodes[tab.childNodes.length - 2].textContent.trim() : tab.textContent.trim();
        // Remove number from text if present
        rawText = rawText.replace(/[0-9]/g, "").trim();
        activeCategory = rawText || "All";
        filterTools();
      });
    });

    if (searchInput) {
      searchInput.addEventListener("input", function (e) {
        activeQuery = e.target.value;
        filterTools();
      });
    }
  }

  // --- ACTIVITY TRACKING ---
  function initActivity() {
    var accordionBtn = document.querySelector("main section.rounded-panel > button");
    if (!accordionBtn) return;

    var countLabel = accordionBtn.querySelector(".text-fg-muted");

    function updateLabel() {
      var clicks = parseInt(localStorage.getItem("np_clicks") || "0", 10);
      var used = JSON.parse(localStorage.getItem("np_used_tools") || "[]").length;
      if (countLabel) {
        countLabel.textContent = clicks + " clicks \xB7 " + used + " tools used";
      }
    }

    updateLabel();

    // Track clicks on tool links
    document.addEventListener("click", function (e) {
      var link = e.target.closest("a");
      if (link && link.closest("article") && link.href) {
        var clicks = parseInt(localStorage.getItem("np_clicks") || "0", 10) + 1;
        localStorage.setItem("np_clicks", clicks.toString());

        var toolTitle = link.closest("article").querySelector("h3")?.textContent || link.href;
        var used = JSON.parse(localStorage.getItem("np_used_tools") || "[]");
        if (used.indexOf(toolTitle) === -1) {
          used.push(toolTitle);
          localStorage.setItem("np_used_tools", JSON.stringify(used));
        }
        updateLabel();
      }
    });

    accordionBtn.addEventListener("click", function () {
      var expanded = accordionBtn.getAttribute("aria-expanded") === "true";
      accordionBtn.setAttribute("aria-expanded", String(!expanded));
      var chevron = accordionBtn.querySelector("svg.lucide-chevron-down");
      if (chevron) {
        chevron.style.transform = expanded ? "" : "rotate(180deg)";
      }
      var panel = document.getElementById("np-activity-panel");
      if (!panel) {
        panel = document.createElement("div");
        panel.id = "np-activity-panel";
        panel.className = "border-t border-line px-5 py-4 sm:px-6";
        accordionBtn.parentNode.appendChild(panel);
      }
      if (!expanded) {
        var used = JSON.parse(localStorage.getItem("np_used_tools") || "[]");
        if (used.length === 0) {
          panel.innerHTML = '<p class="text-sm text-fg-muted">You haven\'t used any tools yet. Pick one from the directory below to get started!</p>';
        } else {
          panel.innerHTML = '<p class="text-xs font-bold uppercase tracking-wider text-fg-muted mb-2">Recently used:</p><ul class="space-y-1">' + used.map(function(t){ return '<li class="text-sm text-fg font-medium">\u2022 ' + escapeHtml(t) + '</li>'; }).join("") + '</ul>';
        }
        panel.style.display = "block";
      } else {
        panel.style.display = "none";
      }
    });
  }

  // --- FAVORITES ---
  function initFavorites() {
    var favButtons = document.querySelectorAll('button[aria-label*="favorites"]');
    var favs = JSON.parse(localStorage.getItem("np_favorites") || "[]");

    favButtons.forEach(function (btn) {
      var card = btn.closest("article");
      var title = card ? card.querySelector("h3")?.textContent.trim() : "";
      var star = btn.querySelector("span");

      if (favs.indexOf(title) !== -1) {
        btn.setAttribute("aria-pressed", "true");
        btn.classList.add("text-cta");
        if (star) star.textContent = "\u2605";
      }

      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        var currentFavs = JSON.parse(localStorage.getItem("np_favorites") || "[]");
        var idx = currentFavs.indexOf(title);
        if (idx !== -1) {
          currentFavs.splice(idx, 1);
          btn.setAttribute("aria-pressed", "false");
          btn.classList.remove("text-cta");
          if (star) star.textContent = "\u2606";
        } else {
          currentFavs.push(title);
          btn.setAttribute("aria-pressed", "true");
          btn.classList.add("text-cta");
          if (star) star.textContent = "\u2605";
        }
        try {
          localStorage.setItem("np_favorites", JSON.stringify(currentFavs));
        } catch (err) {}
      });
    });
  }

  // --- VOICE SEARCH ---
  function initVoiceSearch() {
    var voiceBtn = document.querySelector('header button[aria-label="Search by voice"]');
    var searchInput = document.querySelector('header input[type="search"]');
    if (!voiceBtn || !searchInput) return;

    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      voiceBtn.style.display = "none";
      return;
    }

    var recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;

    voiceBtn.addEventListener("click", function () {
      try {
        recognition.start();
        voiceBtn.classList.add("text-brand");
      } catch (e) {}
    });

    recognition.onresult = function (e) {
      var transcript = e.results[0][0].transcript;
      searchInput.value = transcript;
      searchInput.dispatchEvent(new Event("input", { bubbles: true }));
      voiceBtn.classList.remove("text-brand");
    };

    recognition.onerror = function () {
      voiceBtn.classList.remove("text-brand");
    };

    recognition.onend = function () {
      voiceBtn.classList.remove("text-brand");
    };
  }

  function escapeHtml(str) {
    if (!str) return "";
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
})();

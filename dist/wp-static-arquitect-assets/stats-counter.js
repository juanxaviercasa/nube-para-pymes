/**
 * Nube para Pymes - Dynamic Stats & Counter Engine
 * Synchronizes the number of published posts and tools dynamically
 * and animates counters with smooth easing when in viewport.
 */
(function() {
  'use strict';

  function initStatsSync() {
    const postStatEls = document.querySelectorAll('[data-stat="posts"], .npp-stat-num[data-target]');
    const artAllLinks = document.querySelectorAll('.npp-art-all');

    // 1. Fetch live metrics from /stats.json
    fetch('/stats.json')
      .then(function(res) {
        if (!res.ok) throw new Error('Status ' + res.status);
        return res.json();
      })
      .then(function(data) {
        if (!data) return;
        const postsCount = data.posts_count || data.posts;
        const toolsCount = data.tools_count || data.tools;

        if (postsCount) {
          // Update post counters
          postStatEls.forEach(function(el) {
            const label = el.nextElementSibling ? el.nextElementSibling.textContent.toLowerCase() : '';
            if (el.getAttribute('data-stat') === 'posts' || label.includes('artículo') || label.includes('articulo') || label.includes('entrada')) {
              el.setAttribute('data-target', postsCount);
              if (!el.classList.contains('animating')) {
                el.textContent = postsCount;
              }
            }
          });

          // Update "Ver los X artículos"
          artAllLinks.forEach(function(link) {
            link.innerHTML = 'Ver los ' + postsCount + ' artículos <span aria-hidden="true">&rarr;</span>';
          });
        }

        if (toolsCount) {
          // Update tools counters
          postStatEls.forEach(function(el) {
            const label = el.nextElementSibling ? el.nextElementSibling.textContent.toLowerCase() : '';
            if (el.getAttribute('data-stat') === 'tools' || label.includes('herramienta')) {
              el.setAttribute('data-target', toolsCount);
              if (!el.classList.contains('animating')) {
                el.textContent = toolsCount;
              }
            }
          });
        }
      })
      .catch(function(err) {
        // Fallback silently if offline or cached
        console.debug('Stats sync info: pre-rendered metrics active', err);
      });

    // 2. IntersectionObserver for Smooth Number Roll-up Animation
    const statCards = document.querySelectorAll('.npp-stat-num');
    if (!statCards.length) return;

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion || !('IntersectionObserver' in window)) {
      statCards.forEach(function(el) {
        const target = el.getAttribute('data-target');
        const suffix = el.getAttribute('data-suffix') || '';
        if (target !== null) {
          el.textContent = target + suffix;
        }
      });
      return;
    }

    const observer = new IntersectionObserver(function(entries, obs) {
      entries.forEach(function(entry) {
        if (!entry.isIntersecting) return;
        obs.unobserve(entry.target);
        animateCounter(entry.target);
      });
    }, {
      threshold: 0.2,
      rootMargin: '0px 0px -40px 0px'
    });

    statCards.forEach(function(card) {
      observer.observe(card);
    });

    function animateCounter(el) {
      const target = parseInt(el.getAttribute('data-target'), 10);
      const suffix = el.getAttribute('data-suffix') || '';
      if (isNaN(target)) return;

      if (target === 0) {
        el.textContent = '0' + suffix;
        return;
      }

      el.classList.add('animating');
      const duration = 1200; // ms
      const startTime = performance.now();

      function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Exponential ease-out
        const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
        const currentVal = Math.round(ease * target);

        el.textContent = currentVal + suffix;

        if (progress < 1) {
          requestAnimationFrame(update);
        } else {
          el.textContent = target + suffix;
          el.classList.remove('animating');
        }
      }

      requestAnimationFrame(update);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStatsSync);
  } else {
    initStatsSync();
  }
})();

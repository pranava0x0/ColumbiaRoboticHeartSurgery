/* Hash router for the two audience views. The sections in index.html are the
   source of truth: every <section data-role data-section data-label> becomes a
   tab, in document order. Routes: #patients, #patients/recovery, #physicians/refer. */
(function () {
  'use strict';

  var ROLE_LABEL = { patients: 'For patients', physicians: 'For physicians' };
  var SITE = 'Robotic Coronary Bypass at Columbia';

  var root = document.documentElement;
  root.classList.add('js');

  var home = document.getElementById('home');
  var tabsBar = document.getElementById('tabs');
  var live = document.getElementById('live');
  var sections = Array.prototype.slice.call(
    document.querySelectorAll('section[data-role][data-section]')
  );

  var byRole = {};
  sections.forEach(function (s) {
    if (!byRole[s.dataset.role]) byRole[s.dataset.role] = [];
    byRole[s.dataset.role].push(s);
  });

  Object.keys(byRole).forEach(function (role) {
    var list = document.createElement('div');
    list.className = 'tabs';
    list.setAttribute('role', 'tablist');
    list.setAttribute('aria-label', ROLE_LABEL[role] + ': sections');
    list.dataset.role = role;
    list.hidden = true;
    byRole[role].forEach(function (s) {
      var tab = document.createElement('a');
      tab.className = 'tab';
      tab.id = 'tab-' + s.id;
      tab.href = '#' + role + '/' + s.dataset.section;
      tab.textContent = s.dataset.label;
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', s.id);
      tab.setAttribute('aria-selected', 'false');
      tab.tabIndex = -1;
      list.appendChild(tab);
      s.setAttribute('role', 'tabpanel');
      s.setAttribute('aria-labelledby', tab.id);
      s.tabIndex = -1;
    });
    tabsBar.appendChild(list);
  });

  function parse() {
    var parts = location.hash.replace(/^#\/?/, '').split('/');
    var role = parts[0];
    if (!byRole[role]) return null;
    var wanted = parts[1];
    var panel = byRole[role].filter(function (s) { return s.dataset.section === wanted; })[0];
    return { role: role, panel: panel || byRole[role][0] };
  }

  function render(moveFocus) {
    var view = parse();
    document.body.dataset.view = view ? view.role : 'home';
    home.classList.toggle('is-active', !view);
    home.hidden = !!view;

    sections.forEach(function (s) { s.hidden = !(view && s === view.panel); });

    Array.prototype.forEach.call(tabsBar.querySelectorAll('.tabs'), function (list) {
      var on = !!view && list.dataset.role === view.role;
      list.hidden = !on;
      Array.prototype.forEach.call(list.querySelectorAll('.tab'), function (tab) {
        var selected = on && tab.getAttribute('aria-controls') === view.panel.id;
        tab.setAttribute('aria-selected', selected ? 'true' : 'false');
        tab.tabIndex = selected ? 0 : -1;
      });
    });

    Array.prototype.forEach.call(document.querySelectorAll('.role-switch a'), function (a) {
      if (view && a.dataset.role === view.role) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });

    var title = view ? view.panel.dataset.label + ' · ' + ROLE_LABEL[view.role] + ' · ' + SITE : SITE;
    document.title = title;
    if (live) live.textContent = view ? view.panel.dataset.label + ', ' + ROLE_LABEL[view.role] : 'Start page';
    if (moveFocus && view) view.panel.focus({ preventScroll: true });
    window.scrollTo(0, 0);
  }

  tabsBar.addEventListener('keydown', function (e) {
    var keys = ['ArrowRight', 'ArrowLeft', 'Home', 'End'];
    if (keys.indexOf(e.key) < 0) return;
    var list = e.target.closest ? e.target.closest('.tabs') : null;
    if (!list) return;
    var tabs = Array.prototype.slice.call(list.querySelectorAll('.tab'));
    var i = tabs.indexOf(document.activeElement);
    if (i < 0) return;
    e.preventDefault();
    var n = i;
    if (e.key === 'ArrowRight') n = (i + 1) % tabs.length;
    else if (e.key === 'ArrowLeft') n = (i - 1 + tabs.length) % tabs.length;
    else if (e.key === 'Home') n = 0;
    else n = tabs.length - 1;
    location.hash = tabs[n].getAttribute('href');
    tabs[n].focus();
  });

  window.addEventListener('hashchange', function () {
    // An in-page anchor such as the skip link's #main is not a route; leave the view alone.
    if (location.hash && !parse()) return;
    render(false);
  });

  var themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var dark = root.dataset.theme
        ? root.dataset.theme === 'dark'
        : window.matchMedia('(prefers-color-scheme: dark)').matches;
      root.dataset.theme = dark ? 'light' : 'dark';
      themeBtn.setAttribute('aria-pressed', String(!dark));
    });
  }

  render(false);
})();

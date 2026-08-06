(function () {
  // The initial theme is applied by the inline script in <head> (see
  // partials/head.html) before first paint. This file only handles the
  // "Switch Colors" toggle and persists the choice; colors themselves are
  // driven by the CSS variables in blog.css/cv.css via [data-theme].
  var root = document.documentElement;

  function setTheme(t) {
    root.setAttribute('data-theme', t);
    try { localStorage.setItem('theme', t); } catch (e) {}
  }

  var colorButton = document.getElementById('colorSwitchButton');
  if (colorButton) {
    colorButton.addEventListener('click', function () {
      setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
  }

  var picture = document.getElementById('profile-picture');
  if (picture) {
    picture.addEventListener('click', function () { window.location.href = '/'; });
  }
})();

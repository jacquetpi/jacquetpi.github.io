(function () {
  // Toggles for collapsible publication blocks (.bibtex-block / .abstract-block).
  // The BibTeX snippet is additionally copied to the clipboard when possible.
  function toggleBlock(btn, blockSelector, copy) {
    var article = btn.closest('article');
    if (!article) return;
    var block = article.querySelector(blockSelector);
    if (!block) return;

    var show = block.hidden;
    block.hidden = !show;
    btn.setAttribute('aria-expanded', String(show));

    if (show && copy && navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(block.textContent).then(function () {
        var label = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(function () { btn.textContent = label; }, 1500);
      }, function () { /* clipboard unavailable: snippet stays visible */ });
    }
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.bibtex-toggle');
    if (btn) {
      toggleBlock(btn, '.bibtex-block', true);
      return;
    }
    btn = e.target.closest('.abstract-toggle');
    if (btn) {
      toggleBlock(btn, '.abstract-block', false);
    }
  });
})();

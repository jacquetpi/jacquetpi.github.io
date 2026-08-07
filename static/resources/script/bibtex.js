(function () {
  // Toggles for collapsible publication blocks (.bibtex-block / .abstract-block).
  // Only one block is deployed at a time per entry: opening one closes the other,
  // and each block has a close button. The BibTeX snippet is additionally copied
  // to the clipboard when possible.
  function toggleBlock(btn, blockSelector, copy) {
    var article = btn.closest('article');
    if (!article) return;
    var block = article.querySelector(blockSelector);
    if (!block) return;

    var show = block.hidden;

    if (show) {
      var blocks = article.querySelectorAll('.bibtex-block, .abstract-block');
      for (var i = 0; i < blocks.length; i++) {
        if (blocks[i] !== block) blocks[i].hidden = true;
      }
      var toggles = article.querySelectorAll('.bibtex-toggle, .abstract-toggle');
      for (var j = 0; j < toggles.length; j++) {
        if (toggles[j] !== btn) toggles[j].setAttribute('aria-expanded', 'false');
      }
    }

    block.hidden = !show;
    btn.setAttribute('aria-expanded', String(show));

    if (show && copy && navigator.clipboard && window.isSecureContext) {
      var snippet = block.querySelector('.bibtex-snippet');
      if (!snippet) return;
      navigator.clipboard.writeText(snippet.textContent).then(function () {
        var label = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(function () { btn.textContent = label; }, 1500);
      }, function () { /* clipboard unavailable: snippet stays visible */ });
    }
  }

  document.addEventListener('click', function (e) {
    var close = e.target.closest('.pub-block-close');
    if (close) {
      var block = close.closest('.bibtex-block, .abstract-block');
      var article = close.closest('article');
      if (block) block.hidden = true;
      if (block && article) {
        var selector = block.classList.contains('bibtex-block') ? '.bibtex-toggle' : '.abstract-toggle';
        var toggle = article.querySelector(selector);
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
      }
      return;
    }
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

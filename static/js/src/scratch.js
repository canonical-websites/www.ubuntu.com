(function () {
  // Toogles classes the active and open classes on the footer titles
  var footerTitlesA = document.querySelectorAll("footer li h2");
  footerTitlesA.forEach(function (node) {
    node.addEventListener("click", function (e) {
      e.target.classList.toggle("active");
    });
  });

  /**
   Copies text given as a parameter to clipboard.
   @param {String} str The text value to copy.
   */
  function copyToClipboard(str) {
    // Crate an offscreen textarea to handle copying.
    var copyEl = document.createElement("textarea");
    copyEl.value = str;
    copyEl.setAttribute("readonly", "");
    copyEl.style.position = "absolute";
    copyEl.style.left = "-9999px";
    document.body.appendChild(copyEl);

    // Check for any existing selection range.
    var selectedRange =
      document.getSelection().rangeCount > 0
        ? document.getSelection().getRangeAt(0)
        : false;

    // Select and copy textarea contents.
    // Copy command only works as a result of a user action (e.g. click events).
    copyEl.select();
    document.execCommand("copy");

    document.body.removeChild(copyEl);

    // Restore any previous selection
    if (selectedRange) {
      document.getSelection().removeAllRanges();
      document.getSelection().addRange(selectedRange);
    }
  }

  /**
   Attaches event listener to the copy button
   @param {HTMLElement} codeCopyable The code copyable container element.
   */
  function setupCodeCopyable(codeCopyable) {
    var copyButton = codeCopyable.querySelector(".p-code-copyable__action");

    copyButton.addEventListener("click", function () {
      var clipboardValue = this.previousSibling.previousSibling.value;
      copyToClipboard(clipboardValue);
    });
  }

  // Setup all code copyable blocks on the page.
  var codeCopyables = document.querySelectorAll(".p-code-copyable");

  for (var i = 0, l = codeCopyables.length; i < l; i++) {
    setupCodeCopyable(codeCopyables[i]);
  }
})();

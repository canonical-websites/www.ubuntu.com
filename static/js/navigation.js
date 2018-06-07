var navDropdowns = document.querySelectorAll('.p-navigation__dropdown-link');
var navLinks = document.querySelectorAll('.p-navigation__link-anchor');
var dropdownWindowOverlay = document.querySelector('.dropdown-window-overlay');
var navigationThresholdBreakpoint = 900;

function showMenu(e) {
  e.currentTarget.classList.add('is-hovered');
  dropdownWindowOverlay.classList.add('is-visible');
}

function hideMenu(e) {
  e.currentTarget.classList.remove('is-hovered');
  dropdownWindowOverlay.classList.remove('is-visible');
}

function toggleMenu(e) {
  e.preventDefault();

  var selectedMenu = document.querySelector('.is-hovered');
  var el = e.currentTarget;

  if (selectedMenu) {
    if (selectedMenu === el) {
      selectedMenu.classList.remove('is-hovered');
      dropdownWindowOverlay.classList.remove('is-visible');
    } else {
      el.classList.add('is-hovered');
      selectedMenu.classList.remove('is-hovered');
    }
  } else {
    el.classList.add('is-hovered');
    dropdownWindowOverlay.classList.add('is-visible');
  }
}

function closeAllMenus() {
  var menus = document.querySelectorAll('.is-hovered');

  menus.forEach(function(menu) {
    menu.classList.remove('is-hovered');
  });

  dropdownWindowOverlay.classList.remove('is-visible');
}

function setupDropdowns() {
  navDropdowns.forEach(function(dropdown) {
    if (window.innerWidth < navigationThresholdBreakpoint) {
      dropdown.removeEventListener('mouseenter', showMenu);
      dropdown.removeEventListener('mouseleave', hideMenu);
      dropdown.addEventListener('click', toggleMenu);
      dropdownWindowOverlay.addEventListener('click', closeAllMenus);
    } else {
      dropdown.removeEventListener('click', toggleMenu);
      dropdownWindowOverlay.removeEventListener('click', closeAllMenus);
      dropdown.addEventListener('mouseenter', showMenu);
      dropdown.addEventListener('mouseleave', hideMenu);
    }
  });
}

setupDropdowns();

window.addEventListener('resize', function() {
  setupDropdowns();
});

navLinks.forEach(function(link) {
  link.addEventListener('click', function(e) {
    e.preventDefault();
  });
});

var globalNav = document.querySelector('.global-nav');
var globalNavDropdown = document.querySelector('.global-nav__link--dropdown');
var globalNavContent = document.querySelector('.global-nav__dropdown-content');

globalNavDropdown.addEventListener('click', function(event) {
  event.stopPropagation();
  globalNavDropdown.classList.toggle('is-selected');
  globalNavContent.classList.toggle('u-hide');

  if (window.innerWidth < navigationThresholdBreakpoint) {
    window.scrollTo(0, globalNav.offsetTop);
  }
});

document.addEventListener('click', function(event) {
  if (globalNavDropdown.classList.contains('is-selected')) {
    var clickInsideGlobal = globalNav.contains(event.target);

    if (!clickInsideGlobal) {
      globalNavDropdown.classList.remove('is-selected');
      globalNavContent.classList.add('u-hide');
    }
  }
});

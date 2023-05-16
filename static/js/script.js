// Nav bar icon
let icon = 1;
var menu = document.querySelector('#menu_icon');
function menu_icon() {
  if (icon === 1) {
    menu.innerHTML = "<i class='fa fa-close'></i>";
    icon = 0;
  }

  else {
    menu.innerHTML = "<i class='fa fa-bars'></i>";
    icon = 1;
  }
}
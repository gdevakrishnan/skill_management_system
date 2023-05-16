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

// Carousel
let carousel_image = document.querySelector("#carousel_image");
let left_btn = document.querySelector(".left_btn");
let right_btn = document.querySelector(".right_btn");
let count = 0

function slide_show(count) {
  switch (count) {
    case 1:
      carousel_image.setAttribute("src", "../static/images/programming.jpg");
      break;
      
    case 2:
      carousel_image.setAttribute("src", "../static/images/designing.jpg");
      break;

      case 3:
        carousel_image.setAttribute("src", "../static/images/iot.jpg");
        break;
        
        case 4:
      carousel_image.setAttribute("src", "../static/images/chess.jpg");
      break;
  }
}

left_btn.addEventListener("click", () => {
  if (count > 1) {
    count -= 1
  }
  slide_show(count)
})

right_btn.addEventListener("click", () => {
  if (count < 4) {
    count += 1
  }
  slide_show(count)
})

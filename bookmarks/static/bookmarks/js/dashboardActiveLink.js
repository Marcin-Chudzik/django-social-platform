let section = document.getElementById('section').value;
let link_1 = document.getElementById('dashboard');
let link_2 = document.getElementById('images');
let link_3 = document.getElementById('people');

switch (section) {
  case "dashboard":
    link_1.classList.add("active");
    break;
  case "images":
    link_2.classList.add("active");
    break;
  case "people":
    link_3.classList.add("active");
    break;
}

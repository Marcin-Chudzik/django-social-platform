const panel = document.getElementById('panel');
const overlay = document.getElementById('overlay');
const overlayLogin = document.getElementById('overlayLogin');
const overlayRegister = document.getElementById('overlayRegister');

const displayRegisterForm = () => {
  // Slide overlay to left and show register form.
  overlay.style.left = '29.80%';
  panel.style.boxShadow = '0 5px 5px gray';
  setTimeout("overlayLogin.style.display = 'flex';" +
    "panel.style.boxShadow ='-9px 7px 15px gray';", 2200);
  overlayRegister.style.display = 'none';
};

const displayLoginForm = () => {
  // Slide overlay to right and show login form.
  overlay.style.left = '50%';
  panel.style.boxShadow = '0 5px 5px gray';
  setTimeout("overlayRegister.style.display = 'flex';" +
    "panel.style.boxShadow ='9px 7px 15px gray';", 2200);
  overlayLogin.style.display = 'none';
};

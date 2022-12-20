( function () {
  // Decelerating required variables.
  const jqueryVersion = '3.6.0';
  const siteUrl = 'http://127.0.0.1:8000/';
  const staticUrl = siteUrl + 'static/';
  const minWidth = 100;
  const minHeight = 100;

  function bookmarklet () {
    // Loading styles.
    const cssImport = jQuery('<link>');
    cssImport.attr({
      rel: 'stylesheet',
      type: 'text/css',
      href: staticUrl + 'bookmarks/css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
    });
    jQuery('head').append(cssImport);
    // Loading an HTML template.
    boxHTML = "<div id='bookmarklet'><a href='#' id='close'>&times;</a><h1>Choose image to add:</h1><div class='images'></div>";
    jQuery('body').append(boxHTML);
    // "close" event removing a HTML element from the DOM.
    jQuery('#bookmarklet #close').click(remove => jQuery('#bookmarklet').remove());
    // Collecting and displaying images from current website.
    jQuery.each(jQuery("img[src$='jpg']"), function (index, image) {
      if (jQuery(image).width() >= minWidth && jQuery(image).height() >= minHeight) {
        imageUrl = jQuery(image).attr('src');
        jQuery('#bookmarklet .images').append("<a href='#'><img src='" + imageUrl + "'></a>");
      };
    // If image has been choose, redirect to URL with this image.
    jQuery('#bookmarklet .images a').click(function () {
      let selectedImage = jQuery(this).children('img').attr('src');
      // Hide the bookmarklet.
      jQuery('#bookmarklet').hide();
      // Open a new window to indicate an image to Django service.
      window.open(siteUrl + 'images/create/?url=' + encodeURIComponent(selectedImage) + '&title=' 
      + encodeURIComponent(jQuery('title').text()), '_blank');
    });
    });
  };
  // Checking did jQuery library has been loaded.
  if (typeof window.jQuery != 'undefined') {
    bookmarklet();
  } else {
    // Checking if conflicts will occur.
    let conflict = typeof window.$ != 'undefined';
    // Creating a jquery source script and indicate on Google's API.
    let jquerySourceScript = document.createElement('script');
    jquerySourceScript.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/' + jqueryVersion + '/jquery.min.js');
    // Adding a script tag into DOM's <head> element to be processed.
    document.getElementsByTagName('head')[0].appendChild(jquerySourceScript);
    // Mechanism is allowing to wait till end of script will loaded.
    let attempts = 15;
    (loadJqueryScript = () => {
      // Checking if jQuery is defined.
      if (typeof window.jQuery == 'undefined') {
        if (--attempts > 0) {
          window.setTimeout(arguments.callee, 250);
        } else {
          // Too many attempts, raising an Error.
          alert('An error occurred in jQuery loading process.');
        }
      } else {
        bookmarklet ();
      };
    })();
  };
})();  

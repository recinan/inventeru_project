function forceRef()
{
    
  window.addEventListener('load', function() {
    // Ensure the layout adjusts immediately after the page is fully loaded
    setTimeout(function() {
      $(window).trigger('resize'); // Trigger resize event to recalculate the layout
    }, 100); // Delay the resize trigger by 100 milliseconds
  });


}
function isElementInViewport(element) {
  // Get the position and dimensions of the element
  var rect = element.getBoundingClientRect();

  // Check if the element is within the viewport height
  var windowHeight = window.innerHeight ||  document.documentElement.clientHeight;
  var elementTopInView = rect.top >= 0 && rect.top <= windowHeight;
  var elementBottomInView = rect.bottom >= 0 && rect.bottom <= windowHeight;

  // Check if the element is within the viewport width
  var windowWidth = window.innerWidth || document.documentElement.clientWidth;
  var elementLeftInView = rect.left >= 0 && rect.left <= windowWidth;
  var elementRightInView = rect.right >= 0 && rect.right <= windowWidth;

  // Return true if any of the element's edges are within the viewport
  return (
    (elementTopInView || elementBottomInView) &&
    (elementLeftInView || elementRightInView)
  );
}

// Usage example:
var myDiv = document.getElementById('myDiv');
var isInView = isElementInViewport(myDiv);
console.log(isInView);
// Simple contact form simulation
document.getElementById('contactForm').addEventListener('submit', function (e) {
  e.preventDefault();
  alert('Thank you for contacting me! I’ll reply soon.');
  this.reset();
});

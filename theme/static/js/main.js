document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('filters');
    const radios = form.querySelectorAll('input[type="radio"]');
    const select = document.getElementById('category');

    radios.forEach(function(radio) {
      radio.addEventListener('change', function() {
        form.submit();
      });
    });

    select.addEventListener('change', function() {
      form.submit();
    });
  });
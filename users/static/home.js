// Add event listener to the filter button
document.getElementById('filter-btn').addEventListener('click', function() {
    // Get the selected category
    var category = document.getElementById('filter-category').value;
    
    // Get all rows of the table
    var rows = document.querySelectorAll('table tbody tr');
    
    // Loop through all rows and hide/show based on the selected category
    for (var i = 0; i < rows.length; i++) {
      var rowCategory = rows[i].querySelector('.category').textContent;
      if (category === 'all' || rowCategory === category) {
        rows[i].style.display = '';
      } else {
        rows[i].style.display = 'none';
      }
    }
  });
  
  // Add event listener to the reset button
  document.getElementById('reset-btn').addEventListener('click', function() {
    // Reset the filter to show all categories
    document.getElementById('filter-category').value = 'all';
    
    // Get all rows of the table
    var rows = document.querySelectorAll('table tbody tr');
    
    // Loop through all rows and show them
    for (var i = 0; i < rows.length; i++) {
      rows[i].style.display = '';
    }
  });
  

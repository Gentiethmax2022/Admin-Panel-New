function searchTable() {
  // Get the user's search query
  var input = document.getElementById("searchInput");
  var filter = input.value.toUpperCase();
  
  // Get the table element and all rows
  var table = document.getElementById("transactionTable");
  var rows = table.getElementsByTagName("tr");
  
  // Loop through all rows and hide those that don't match the search query
  for (var i = 0; i < rows.length; i++) {
    var description = rows[i].getElementsByTagName("td")[1];
    if (description) {
      var text = description.textContent || description.innerText;
      if (text.toUpperCase().indexOf(filter) > -1) {
        rows[i].style.display = "";
      } else {
        rows[i].style.display = "none";
      }
    }
  }
}



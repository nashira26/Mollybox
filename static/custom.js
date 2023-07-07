function searchFunction() {
   // Get input value and convert to lowercase
   var input = document.getElementById("searchInput");
   var filter = input.value.toLowerCase();

   // Get table and table rows
   var table = document.getElementById("myTable");
   var rows = table.getElementsByTagName("tr");

   // Initialize flag for no results found
   var noResultsFound = true

   // Iterate through table rows
   for (var i = 0; i < rows.length; i++) {
      var cells = rows[i].getElementsByTagName("td");
      var found = false;

       // Iterate through cells in each row
      for (var j = 0; j < cells.length; j++) {
         var cell = cells[j];

         // Check if cell content matches search term
         if (cell.innerHTML.toLowerCase().indexOf(filter) > -1) {
            found = true;
            break;
         }
      }

         // Show/hide row based on search results
      if (found) {
         rows[i].style.display = "";
         noResultsFound = false;
      } else {
         rows[i].style.display = "none";
      }
   }
 // Show/hide no results row
   var noResultsRow = document.getElementById("noResultsRow");
   noResultsRow.style.display = noResultsFound ? "table-row" : "none";
}
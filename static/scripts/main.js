//Initiate jQuery on load.
$(function() {
  //Translate text with flask route
  $("#train").on("click", function(e) {
    e.preventDefault();
    var fileUrl = document.getElementById("file_url").value;
    var numFields = document.getElementById("numfields").value;
    var numNeigbours = document.getElementById("numNearestNeigbours").value;
    var trainRequest = { 'url': fileUrl, 'field': numFields, 'neigbour': numNeigbours }

    if (numNeigbours !== "") {
      $.ajax({
        url: '/train',
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        dataType: 'json',
        data: JSON.stringify(trainRequest),
        success: function(data) {

          console.log(data)
          for (var i = 0; i < data.length; i++) {
            document.getElementById("train-result").textContent += data[i];
          }
        }

      });
    };
  });

})
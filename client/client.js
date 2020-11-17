function init() {

}

function findAll() {
  console.log("pappappero")
  $.ajax({
    url: "https://localhost:5001/api/ElencoIndici", 
    type: "GET",
    contentType: "application/json",
    success: function (result) {
      readResult(JSON.stringify(result));
    },
    error: function (xhr, status, p3, p4) {
      var err = "Error " + " " + status + " " + p3;
      if (xhr.responseText && xhr.responseText[0] == "{")
        err = JSON.parse(xhr.responseText).message;
      alert(err);
    }
  });
}

function readResult(str) {
  document.getElementById('txtarea').value = ""
  document.getElementById('txtarea').value += str;
}


function findById() {
  var id = $('#colId').val();
  $.ajax(
    {
      url: "https://localhost:5001/api/ElencoIndici/" + id,
      type: "GET",
      contentType: "application/json",
      data: "",
      success: function (result) {
        readAtSeparatedResult(JSON.stringify(result));
      },
      error: function (xhr, status, p3, p4) {
        var err = "Error " + " " + status + " " + p3;
        if (xhr.responseText && xhr.responseText[0] == "{")
          err = JSON.parse(xhr.responseText).message;
        alert(err);
      }
    });
}

//str contiene valori separati da un carattere @; elimino @ e stampo un valore per riga
function readAtSeparatedResult(str) {
  document.getElementById('txtarea').value = "";
  str.split('@').forEach(s => document.getElementById('txtarea').value += '\n' + s);
}
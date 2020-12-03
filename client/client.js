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


//questa funzione non viene piu usata in teoria
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


//parte sotto gestisce l'immagine

function getIndexById() {
	var id = $('#colId').val();
	$.ajax({
		url: "https://localhost:5001/api/ElencoIndici/" + id,
		type: "GET",
		contentType: "application/json",
		data: "",
		success: function(result) {
			console.log(result);
			showResult(JSON.parse(result));
		},
		error: function(xhr, status, p3, p4) {
			var err = "Error " + " " + status + " " + p3;
			if (xhr.responseText && xhr.responseText[0] == "{")
				err = JSON.parse(xhr.responseText).message;
			alert(err);
		}
	});
}

function showResult(res) {
	document.getElementById('txtarea').value = "";
	document.getElementById('txtarea').value += res.text;
	renderImage(res.img);
}

function renderImage(base64imageString) {
	var baseStr64 = base64imageString;
	baseStr64 = baseStr64.substring(0, baseStr64.length-1); // tolgo l'ultimo carattere della stringa che codifica l'immagine ("'")
	baseStr64 = baseStr64.substring(2, baseStr64.length); // tolgo i primi due caratteri della stringa che codifica l'immagine ("b'")
	var image = new Image();
	image.src = 'data:image/png;base64,' + baseStr64; // dico che l'immagine è una png codificata in base64 e fornisco l'immagine codificata vera e propria ("baseStr64")
	document.body.appendChild(image);
}
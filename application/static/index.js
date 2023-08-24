$('#bar').hide();
$('#spinner').hide();

var xhttp = new XMLHttpRequest();
function strUcFirst(a){return (a+'').charAt(0).toUpperCase()+a.substr(1);}
function clearSearch() {
    if(document.getElementById("searchForm").value == ""){
        var search ="color";
        loadSearch(search);
    }
}
function loadSearch(search) {
    $('#bar').show();
$('#spinner').show();
  if(search == "search"){
    var search = document.getElementById("searchForm").value;
  }

  document.getElementById("name").textContent=search;
  var url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + search;
  xhttp.open("GET", url, true);
  xhttp.send();

  var imgUrl = "https://source.unsplash.com/featured/?"+ search;
//  var imgUrl = "https://api.unsplash.com/search/photos?query=" + search;
  document.getElementById("searchImage").innerHTML = "<img  src='"+imgUrl+"' loading='lazy' class='img-thumbnail'></img>"
}

xhttp.onreadystatechange = function() {
    if(xhttp.readyState == 4 && xhttp.status == 200) {
        document.getElementById("definition").innerHTML = " ";
        var response = JSON.parse(xhttp.responseText);
        document.getElementById("name").innerHTML = strUcFirst(response["0"].word);
        i = 0;
        while(i != response[0].meanings[0].definitions.length) {
            $('#bar').hide();
            $('#spinner').hide();

            document.getElementById("definition").innerHTML +="<div id='definitions' class='definition'><i class='bi bi-caret-right'></i>"+strUcFirst(response['0']['meanings']['0']['definitions'][i].definition)+"</div></hr>"
            i += 1;
        }
    }
    else if(xhttp.status != 200) {
        $('#bar').hide();
        $('#spinner').hide();

        document.getElementById("definition").innerHTML = "<h2>No meaning found</h2>";
        var imgUrl = "https://source.unsplash.com/featured/?404";
        document.getElementById("searchImage").innerHTML = "<img src='"+imgUrl+"'class='img-thumbnail' crossorigin='anonymous'></img>"

    }
}
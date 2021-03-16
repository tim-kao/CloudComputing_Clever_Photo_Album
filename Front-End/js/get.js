
function searchPhoto() {

  var apigClient = apigClientFactory.newClient({
    apiKey: API_KEY
  });

  var image_message = document.getElementById("note-textarea").value;
  if(image_message == "")
    var image_message = textBox.value;
  console.log(image_message);

  var body = {};
  var params = {
    q: image_message,
    'X-Api-Key': API_KEY
  };
  var additionalParams = {
    headers: {
      'Content-Type': "application/json",
    },
  };

  apigClient.searchGet(params, body)
    .then(function (result) {
      var img1 = result.data;
      console.log(img1.length);
      if (img1.length == 0) {
        document.getElementById("img-container").innerHTML = "";
        document.getElementById("search_result").innerHTML = "Search not found";
      }
      document.getElementById("search_result").innerHTML = "";
      document.getElementById("img-container").innerHTML = "";
      var para = document.createElement("p");
      para.setAttribute("id", "displaytext")
      document.getElementById("img-container").appendChild(para);
      console.log(img1);
      img1.forEach(function (obj) {
        var img = new Image();
        // img.src = "https://photosforsearch1.s3.amazonaws.com/"+obj;
        img.src = obj;
        console.log(obj);
        img.setAttribute("class", "banner-img");
        img.setAttribute("alt", "images");
        img.setAttribute("width", "200");
        img.setAttribute("height", "150");
        document.getElementById("search_result").innerHTML = "Search done";
        document.getElementById("img-container").appendChild(img);

      });
    }).catch(function (result) {
      //This is where you would put an error callback
      document.getElementById("search_result").innerHTML = "Search not found";
    });

}

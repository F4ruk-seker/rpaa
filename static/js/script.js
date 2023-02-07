function goCalculate() {
    analizeText =  document.querySelector("#analizetext");
    sonucLabel = document.querySelector("#result");
    fetch('/calculate?text='+analizeText.value)
    .then(function (response) {
        return response.json();
    }
    //then parser
    )
    .then(function (text) {
          if (text.err == true) {
            sonucLabel.classList = "text-danger"
            sonucLabel.innerText = "lütfen Yorum Giriniz";
          }//if
          else{
            sonucLabel.classList = "text-secondary"
            sonucLabel.innerText = "Sonuç : "+text.result;
          }//else
        }//then JSON Verisinin islenmesi
      )//then END
    }//function END

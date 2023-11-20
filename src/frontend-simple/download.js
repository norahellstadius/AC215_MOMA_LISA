function download_test() {
      var a = document.createElement('a');
      a.href = "images/seb.png";
      a.download = "NORAÄRBÄST.JPG";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    };
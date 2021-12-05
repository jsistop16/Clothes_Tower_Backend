<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Camera API</title>
        <link rel="stylesheet" href="css/base.css" type="text/css" media="screen">
    </head>
 
    <body>
 
        <div class="container">
            <h1>Camera API</h1>
 
            <section class="main-content">
                <p>A demo of the Camera API, currently implemented in Firefox and Google Chrome on Android. Choose to take a picture with your device's camera and a preview will be shown through createObjectURL or a FileReader object (choosing local files supported too).</p>
 
                <p>
                    <input type="file" id="take-picture" accept="image/*">
                </p>
 
                <h2>Preview:</h2>
                <p>
                    <img src="about:blank" alt="" id="show-picture">
                </p>
 
                <p id="error"></p>
 
            </section>
 
            <p class="footer">All the code is available in the <a href="https://github.com/robnyman/robnyman.github.com/tree/master/camera-api">Camera API repository on GitHub</a>.</p>
        </div>
 
 
        <script src="js/base.js"></script>
 
 
    </body>
</html>
JavaScript 파일
(function () {
    var takePicture = document.querySelector("#take-picture"),
        showPicture = document.querySelector("#show-picture");
 
    if (takePicture &amp;&amp; showPicture) {
        // 이벤트 설정
        takePicture.onchange = function (event) {
            // 찍은 사진이나 파일에 대한 참조 얻기
            var files = event.target.files,
                file;
            if (files && files.length > 0) {
                file = files[0];
                try {
                    // window.URL 객체 얻기
                    var URL = window.URL || window.webkitURL;
 
                    // ObjectURL 생성
                    var imgURL = URL.createObjectURL(file);
 
                    // src에 ObjectURL 지정
                    showPicture.src = imgURL;
 
                    // Revoke ObjectURL
                    URL.revokeObjectURL(imgURL);
                }
                catch (e) {
                    try {
                        // createObjectURL을 지원하지 않는 경우 대안
                        var fileReader = new FileReader();
                        fileReader.onload = function (event) {
                            showPicture.src = event.target.result;
                        };
                        fileReader.readAsDataURL(file);
                    }
                    catch (e) {
                        //
                        var error = document.querySelector("#error");
                        if (error) {
                            error.innerHTML = "Neither createObjectURL or FileReader are supported";
                        }
                    }
                }
            }
        };
    }
})();
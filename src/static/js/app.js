let token = "";

$(window).scroll(function() {
    if($(window).scrollTop() + $(window).height() >= $(document).height()) {
        const Http = new XMLHttpRequest();
        const url = "http://127.0.0.1:5000/urls ";
        Http.open("POST", url, true);
        Http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        Http.send(`key=token&token=${token}`);
        Http.onreadystatechange=(e)=>{
            token = Http.responseText
            }
    }
});
$(function() {
    $("#RunButton").click(function() {
        var sentence = $("#sentence").val();
        window.location.href = "/index?sentence="+sentence;
    })
});
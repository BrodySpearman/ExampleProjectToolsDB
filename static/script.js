$(document).ready(function() {
    console.log("Hello! Jquery loaded in js file");
});

$(document).ready(function () {
    //preload dialogue
    $("#dialog").dialog({
        autoOpen: false,
        minWidth: 450
    });

    $("#add-record-btn").click(function () {
        $("#dialog").dialog("open");
    });
});



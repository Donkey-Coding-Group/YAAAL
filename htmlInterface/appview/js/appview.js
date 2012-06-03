
$(window).load(function() {
    options = $('#options');
});

function optionsPressed(node, event) {
    options.fadeIn();
}

function cancelOptions(node, event) {
    options.fadeOut();
}

function saveOptions(node, event) {
    // TODO: implemented saving here.
    options.fadeOut();
}



function successDialog(message) {
    alert(message);
}

function faildDialog(message) {
    alert(message);
}

$(window).load(function() {
    $('button.app-add-btn').click(function () {

        var self = $(this.parentNode.parentNode);
        var index = this.getAttribute('app-index');
        if (index == undefined) {
            return;
        }

        $.ajax({
            url: '/api/add-app/' + index,
            success: function (data) {
                try {
                    data = JSON.parse(data);
                }
                catch (e) {
                    failDialog("Server returned invalid JSON.");
                    return;
                }

                if (data.status == 'OK') {
                    self.fadeOut(1, function () {
                        self.remove()
                    });
                }
                else {  
                    failDialog("Could not register application.");
                }
            },
        });

    });
    $('button.app-rm-btn').click(function () {

        var self = $(this.parentNode.parentNode);
        var index = this.getAttribute('app-index');
        if (index == undefined) {
            return;
        }

        $.ajax({
            url: '/api/rm-app/' + index,
            success: function (data) {
                try {
                    data = JSON.parse(data);
                }
                catch (e) {
                    failDialog("Server returned invalid JSON.");
                }

                if (data.status == 'OK') {
                    self.fadeOut(1, function () {
                        self.remove()
                    });
                }
                else {
                    failDialog("Could not remove application.");
                }
            }
        });
    });
});










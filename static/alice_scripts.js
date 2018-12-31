$(document).ready(function () {
    $("#sync").click(function () {

        $.ajax({
            type: "GET",
            url: "/burrow/demo/check/data/",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                if (data.err) {
                    $("#message").html('<div class="alert alert-danger"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a><strong>Warning! </strong>' + data.msg + '</div>')
                }
                else {
                    $("#message").html('<div class="alert alert-success"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a><strong>Success! </strong>' + data.msg + '</div>')
                }
            }
        });
    });

    $(".edit_ham").click(
        function () {
            var ham_id = $(this).attr('id');
            ham_id = ham_id.substr(5);
            $('.modal-title').html('Edit ' + $('.ham_name_' + ham_id).val());

            $.getJSON("/burrow/demo/info/" + ham_id+"/", function (result) {
                $("#name").val(result.name);
                $("#price").val(result.price);
                $("#amount").val(result.amount);
                $("#ham_id").val(ham_id);
            });

            $("#modal").modal();
        }
    );

    $(".valid_ham").click(
        function () {
            var ham_id = $(this).attr('id');
            ham_id = ham_id.substr(6);

            var ham_name = $('#ham_name_'+ham_id).val();
            $('.modal-title').html('Edit ' + $('.ham_name_' + ham_id).val());

            $.getJSON("/burrow/demo/validate/" + ham_id+"/", function (result) {
                if (result.is_valid === 'true') {
                    $("#message").html('<div class="alert alert-success"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a><strong>Success! </strong>'+ham_name+' is identical within a chain one</div>')

                }
                else {
                    $("#message").html('<div class="alert alert-danger"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a><strong>Warning! </strong>'+ham_name+' is not identical within a chain</div>')
                }
            });

        }
    );

    $(".del_ham").click(
        function () {
            var ham_id = $(this).attr('id');
            ham_id = ham_id.substr(4);

            $.ajax({
                type: "GET",
                url: "/burrow/demo/delete/" + ham_id+"/",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function (data) {
                    if (data.err) {
                        $("#message").html('<div class="alert alert-danger"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a><strong>Warning! </strong>' + data.msg + '</div>')
                    }
                    else {
                        $("#message").html('<div class="alert alert-success"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a><strong>Success! </strong>' + data.msg + '</div>')
                    }
                }
            });
        }
    );

    $("#save_ham").click(
        function () {
            var ham_id = $("#ham_id").val();
            var name = $("#name").val();
            var price = $("#price").val();
            var amount = $("#amount").val();

            $.ajax({
                type: "POST",
                url: "/burrow/demo/update/"+ham_id+"/",
                data: JSON.stringify({ name: name, price: price, amount: amount }),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function (data) {
                    if (data.err) {
                        $("#message").html('<div class="alert alert-danger"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a><strong>Warning! </strong>' + data.msg + '</div>')
                    }
                    else {
                        $("#message").html('<div class="alert alert-success"><a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a><strong>Success! </strong>' + data.msg + '</div>')
                    }
                }
            });

            $("#modal").modal("hide");
        }
    );
});
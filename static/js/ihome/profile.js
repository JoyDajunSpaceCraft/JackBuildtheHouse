function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {
    $.get('/api/v1/user/', function (data) {
        $('#user-avatar').attr('src', data.user.avatar);
        $('#user-name').val(data.user.name);
    });
});

$('#form-avatar').submit(function () {
    $('#error_msg1').hide();
    $(this).ajaxSubmit({
        url: "/api/v1/user/",
        type: "put",
        dataType: "json",
        success: function (data) {
            if (data.code == RET.OK) {
                $('#user-avatar').attr('src',data.url);

            } else {
                $('#error_msg1').show();
            }
        }
    });
    return false;
});

$('#form-name').submit(function () {
    $('#error_msg2').hide();
    $.ajax({
        url:'/api/v1/user/',
        type:'put',
        data:{'name':$('#user-name').val()},
        success:function (data) {
            if(data.code==RET.OK){
                //
            }else{
                $('#error_msg2').show();
            }
        }
    });
    return false;
});

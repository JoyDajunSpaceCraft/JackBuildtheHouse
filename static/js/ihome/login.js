function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        $('#result-err').hide();

        //阻止表单的提交，而改为使用ajax提交
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        //提交
        $.post('/api/v1/user/session?token='+TOKEN,
            $(this).serialize(),
            function (data) {
            if(data.code==RET.OK){
                // location.href='my.html';
                location.href='my2.html';
            }else{
                $('#result-err').show().find('span').html(data.msg);
            }
        });
    });
})

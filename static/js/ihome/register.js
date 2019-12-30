function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

//生成图片验证码
function generateImageCode() {
    var src=$('#image_code').attr('src')+1;
    $('#image_code').attr('src',src);
}

//发送短信验证码
function sendSMSCode() {
    //点击后不可再点击
    $(".phonecode-a").removeAttr("onclick");
    $('#phone-code-err').hide();
    //获取手机号
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    //获取图片验证码
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    //如果手机号、图片验证码都已经填写，则发起ajax请求，让服务器向指定手机号发送短信验证码
    $.get('/api/v1/user/send_sms',
        {'mobile':mobile,'imageCode':imageCode},
        function (data) {
            if(data.code!=MESSAGE.OK){
                $('#phone-code-err').show().find('span').html(data.msg);
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
            }
        }
    );
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
    $(".form-register").submit(function(){
        //验证填写的数据是否合法
        //....
        //调用api完成注册
        $('#result-err').hide();
        $.post('/api/v1/user/',
            $(this).serialize(),//表单序列化{name:value,name:value,...}
            function (data) {
                if(data.code==MESSAGE.OK){
                    location.href='/login.html';
                }else{
                    $('#result-err').show().find('span').html(data.msg);
                }
            }
        );
        return false;
    });
})

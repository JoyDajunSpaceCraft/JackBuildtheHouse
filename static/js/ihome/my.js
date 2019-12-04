function logout() {
    $.ajax({
        url:'/api/v1/user/session',
        type:'DELETE',
        success:function (data) {
            if(data.code==RET.OK) {
                location.href = '/index.html';
            }
        }
    });
}

$(document).ready(function(){
    $.get('/api/v1/user/',function (data) {
        $('#user-avatar').attr('src',data.user.avatar);
        $('#user-name').html(data.user.name);
        $('#user-mobile').text(data.user.phone);
    });
})
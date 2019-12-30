$(document).ready(function () {
  $.get('/api/v1/order/', function (data) {
    var html = template('orders', {olist: data.olist});
    console.log(html);
  });
});
function logout() {
    $.ajax({
        url:'/api/v1/user/session',
        type:'DELETE',
        success:function (data) {
            if(data.code==MESSAGE.OK) {
                location.href = '/index.html';
            }
        }
    });
}


function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
        },1000)
    });
}

$.get('/api/v1/user/auth',function (data) {
    $('#real-name').val(data.id_name);
    $('#id-card').val(data.id_card);
    if(data.id_name!=null) {
        $('.btn-success').hide();
    }
});



$('#form-auth').submit(function () {
  console.log($('#real-name').val());
  console.log($('#id-card').val());
    $.ajax({
        url:'/api/v1/user/auth',
        type:'put',
        data:{
            id_name:$('#real-name').val(),
            id_card:$('#id-card').val()
        },
        success:function (data) {
            if(data.code==MESSAGE.OK){
                $('.btn-success').hide();
                showSuccessMsg();
            }else{
                $('.error-msg').show().find('span').html(ret_map[data.code]);
            }
        }
    });
    return false;
});

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

//查询地区、设施信息
$.get('/api/v1/house/area_facility',function (data) {
    //地区
    var area_html=template('area_list',{area_list:data.area});
    $('#area-id').html(area_html);
    //设施
    var facility_html=template('facility_list',{facility_list:data.facility});
    $('.house-facility-list').html(facility_html);
});

//为房屋表单绑定提交事件
$('#form-house-info').submit(function () {
    $('.error-msg text-center').hide();
    //验证内容是否填写
    $.post('/api/v1/house/',$(this).serialize(),function (data) {
        if(data.code==RET.OK){
            $('#form-house-info').hide();
            $('#form-house-image').show();
            $('#house-id').val(data.house_id);
        }else{
            $('.error-msg text-center').show().find('span').html(ret_map[data.code]);
        }
    });
    return false;
});

//为图片表单绑定事件
$('#form-house-image').submit(function () {
    $(this).ajaxSubmit({
        url: "/api/v1/house/image",
        type: "post",
        dataType: "json",
        success: function (data) {
            if (data.code == RET.OK) {
                $('.house-image-cons').append('<img src="'+data.url+'"/>');
            }
        }
    });
    return false;
});

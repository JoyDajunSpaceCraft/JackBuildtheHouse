function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
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

$(document).ready(function () {
  var id = decodeQuery()['id'];
  console.log(id);
  $.get('/api/v1/house/old_form/' + id, function (data) {
    // 默认显示原始房源数据
    var old_form1 = template('old_form1', {house_list: data.hlist});
    $('.old_form1').html(old_form1);
  });

});

//为房屋表单绑定提交事件
$('#form-house-info').submit(function () {
  $('.error-msg text-center').hide();
  //验证内容是否填写

  $.post('/api/v1/house/change_house' + id, $(this).serialize(), function (data) {
    if (data.code == MESSAGE.OK) {
      $('#form-house-info').hide();
      $('#form-house-image').show();
      $('#house-id').val(data.house_id);
        }else{
            $('.error-msg text-center').show().find('span').html(ret_map[data.code]);
            //显示内容

        }
    });
    return false;
});

//为图片表单绑定事件
// $('#form-house-image').submit(function () {
//     $(this).ajaxSubmit({
//         url: "/api/v1/house/image",
//         type: "post",
//         dataType: "json",
//         success: function (data) {
//             if (data.code == MESSAGE.OK) {
//                 $('.house-image-cons').append('<img src="'+data.url+'"/>');
//             }
//         }
//     });
//     return false;
// });

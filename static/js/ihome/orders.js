//模态框居中的控制
function centerModals() {
  $('.modal').each(function (i) {   //遍历每一个模态框
    var $clone = $(this).clone().css('display', 'block').appendTo('body');
    var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
    top = top > 0 ? top : 0;
    $clone.remove();
    $(this).find('.modal-content').css("margin-top", top - 30);  //修正原先已经有的30个像素
  });
}

function getCookie(name) {
  var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
  return r ? r[1] : undefined;
}

$(document).ready(function () {
  $('.modal').on('show.bs.modal', centerModals);
  //当模态框出现的时候
  $(window).on('resize', centerModals);
  $(".order-comment").on("click", function () {
    console.log("click comment");
    var orderId = $(this).parents("li").attr("order-id");
    $(".modal-comment").attr("order-id", orderId);
  });

  $.get('/api/v1/order/', function (data) {
    var html = template('orders_list', {olist: data.olist});
    $('.orders-list').html(html);
    $('.order-pay').on("click", function () {
      var orderId = $(this).parents("li").attr("order-id");
      $(".modal-pay").attr("order-id", orderId);
      console.log($(".modal-pay").attr("order-id"));
      // 测试是否绑定属性值
    });
  });
  $(".modal-pay").click(function () {
    console.log("click pay");
    //实现模拟支付功能
    var orderId = $(this).attr('order-id');
    console.log(orderId);
    $.ajax({
      url: '/api/v1/order/' + orderId,
      type: 'put',
      data: {'status': 'PAID'},
      success: function (data) {
        $('#pay-modal').modal("hide");
        $('.order-operate').hide();
        $('#' + orderId).text('已付款');
      }
    });
  });

});

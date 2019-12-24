$(document).ready(function () {
  $.get('/api/v1/order/', function (data) {
    var html = template('orders', {olist: data.olist});
    console.log(html)
  });
});

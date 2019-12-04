//获取用户信息，判断是否进行过实名认证
$.get('/api/v1/house/',function (data) {
    if(data.code==RET.OK){
        //已经完成实名认证
        $('#houses-list').show();
        var html=template('house_list',{hlist:data.hlist});
        $('#houses-list').append(html);
    }else if(data.code==RET.USERERR){
        //未实名认证
        $('#auth-warn').show();
    }
});

// 获取该页面的评论
$(function () {
    var pathname = window.location.pathname // 获取当前域名的路径名称
    console.log(pathname)
    console.log('fdsfdsfsfsjdlfdsjfldsj')
    $.ajax({
     url: '/comment',
     type: 'GET',
     dataType: 'json',
     timeout: 1000,
     cache: true,
     data:{'pathname':pathname},
     beforeSend: LoadFunction, //加载执行方法
     error: erryFunction, //错误执行方法
    //  async: false,
     success: succFunction //成功执行方法
    })
    function LoadFunction() {
    //  $("#list").html('加载中...');
    console.log('加载中。。。')
    }
    function erryFunction() {
     alert("error");
    }
    function succFunction(tt) {
     var json = eval(tt); //数组
     var html_var = '';
     var comments = json.data
     if (json.code == 200 ){
        $.each(comments, function (index, item) {
            html_var += "<div class='media'><div class='media-left'><a href='/user_page/"+ item.usr_name +"'>" +
                "<img class='media-object' src="+ item.usr_avaster +" alt='...' style='width:40px;'>" +
                "</a> </div> <div class='media-body'> <h4 class='media-heading'>"+item['usr_name'] +
                " <small class='mute'>"+ item.timestamp +"</small></h4>" + item.msg +"</div></div>"
            console.log(item);
            });
        $('#all_comments').append(html_var);
    //  
     }
     }
   });
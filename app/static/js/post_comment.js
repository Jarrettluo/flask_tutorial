
$("#submit-comment").click(function(){
    // alert("点击了提交按钮");
    var comment =$("#post-comment").val();
    var title=$("#article-detail-title").text()
    var username=$("#article-detail-user").text()
    if(comment || comment==""){
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/comment",
            headers:{
                "Content-Type": "application/json;charset=utf-8"
            },
            contentType:'application/json; charset=utf-8',
            data:JSON.stringify({comment:comment,
                                title:title,
                                username:username}),
            success:succFunction,
        });
    }
    else{
        console.log('空值');
    }
    function succFunction(json) {
        $("#post-comment").val(""); //输入框置为空
        alert("评论成功！")
        var json = eval(json); //数组
         var html_var = '';
         var comments = json.data
         if (json.code == 200 ){
            var item = json.data // 返回的评论数据
            html_var += "<div class='media'><div class='media-left'><a href='/user_page/"+ item.usr_name +"'>" +
                "<img class='media-object' src="+ item.usr_avaster +" alt='...' style='width:40px;'>" +
                "</a> </div> <div class='media-body'> <h4 class='media-heading'>"+item['usr_name'] +
                " <small class='mute'>"+ item.timestamp +"</small></h4>" + item.msg +"</div></div>"

            $('#all_comments').append(html_var);
            }else{
            console.log('数据获取错误')
         }
         }
});


// 当DOM结构加载完成的时候执行
// 获取该页面的评论
$(function () {
    update_comments()
   });

// 更新数据
function update_comments(){
    var pathname = window.location.pathname // 获取当前域名的路径名称
    $.ajax({
         url: '/comment',
         type: 'GET',
         dataType: 'json',
         timeout: 1000,
         cache: true,
         data:{'pathname':pathname},
         beforeSend: LoadFunction, //加载执行方法
         error: erryFunction, //错误执行方法
         success: succFunction //成功执行方法
    })
    function LoadFunction() {
        //  $("#list").html('加载中...');
        // console.log('加载中。。。')
    }
    function erryFunction() {
        // alert("error");
    }
    function succFunction(tt) {
     var json = eval(tt); //数组
     var html_var = '';
     var comments = json.data
     console.log(comments)
     if (json.code == 200 ){
        $.each(comments, function (index, item) {
            html_var += "<div class='media'><div class='media-left'><a href='/user_page/"+ item.usr_name +"'>" +
                "<img class='media-object' src="+ item.usr_avaster +" alt='...' style='width:40px;'>" +
                "</a> </div> <div class='media-body'> <h4 class='media-heading'>"+item['usr_name'] +
                " <small class='mute'>"+ item.timestamp +"</small></h4>" + item.msg +"</div></div>"
            console.log(item);
            });
        $('#all_comments').append(html_var);
        }else{
        console.log('数据获取错误')
     }
     }
}
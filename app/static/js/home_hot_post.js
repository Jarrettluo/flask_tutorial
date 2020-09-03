$(function () {
    $.ajax({
     url: '/recommend',
     type: 'GET',
     dataType: 'json',
     timeout: 1000,
     cache: false,
     beforeSend: LoadFunction, //加载执行方法
     error: erryFunction, //错误执行方法
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
    //  $("#list").html('');
     //eval将字符串转成对象数组
     //var json = { "id": "10086", "uname": "zhangsan", "email": "zhangsan@qq.com" };
     //json = eval(json);
     //alert("===json:id=" + json.id + ",uname=" + json.uname + ",email=" + json.email);
     var json = eval(tt); //数组
     var html_info = ''
     $.each(json, function (index, item) {
         console.log(json)
         var post_id = json[index].post_id
         var post_title = json[index].title
         var post_time = json[index].timestamp
         var post_body = json[index].post_body
        //  http://127.0.0.1:5000/article_detail/1#
         html_info = html_info + "<div class='row' style='margin-bottom:0px;'> <div class='col-md-8'>"
          + "<h4 class='blog-post-title' style='font-weight:bold;'><a href="+
           post_id +">" + post_title +
           "</a> </h4> </div> <div class='col-md-4'> <p class='text-right' style='margin-top:10px;margin-bottom:0px;'>" +
            post_time + "</p></div></div> <p>" + post_body + "</p><hr style='margin-bottom:2px;margin-top:1px;'>"
    });
    $('#recommend_content').append(html_info);
    console.log(html_info)
      //循环获取数据
    //   var name = json[index].Name;
    //   var idnumber = json[index].IdNumber;
    //   var sex = json[index].Sex;
    //   $("#list").html($("#list").html() + "<br>" + name + " - " + idnumber + " - " + sex + "<br/>");

    }
   }); 
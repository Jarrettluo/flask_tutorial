$(function () { 
    $.ajax({ 
     url: '/recommend', 
     type: 'GET', 
     dataType: 'json', 
     timeout: 2000, 
     cache: true, 
     beforeSend: LoadFunction, //加载执行方法 
     error: erryFunction, //错误执行方法 
     success: succFunction //成功执行方法 
    }) 
    function LoadFunction() {
//        console.log('加载中。。。')
    } 
    function erryFunction() { 
        // console.log(err)
        //  alert("error");
    } 
    function succFunction(res) {
     var json = eval(res); //数组
     var html_info = ''

     $.each(json, function (index, item) { 
         console.log(json)
         var post_id = json[index].post_id
         var post_title = json[index].title
         var post_time = json[index].timestamp
         var post_body = json[index].post_body
         html_info = html_info + "<div class='row' style='margin-bottom:0px;'> <div class='col-md-8'>"
          + "<h4 class='blog-post-title' style='font-weight:bold;'><a href="+
           post_id +">" + post_title +
           "</a> </h4> </div> <div class='col-md-4'> <p class='text-right' style='margin-top:10px;margin-bottom:0px;'>" +
            post_time + "</p></div></div> <p>" + post_body + "</p><hr style='margin-bottom:2px;margin-top:1px;'>"
    }); 
    $('#recommend_content').append(html_info);
    }
   });

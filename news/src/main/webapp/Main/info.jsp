<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script src="/news/js/jquery.js"></script>
	<script src="/news/js/bootstrap.min.js"></script>
	<link rel="stylesheet" href="/news/css/bootstrap.min.css">
	
	<style>
		.myin {
			display: block;
			width: 100%;
			margin: 10px;
			padding: 20px;
			border-radius: 5px;
		}
	</style>
</head>

<body>

<div class="container">
<div class="page-header">
		<h1>修改密码</h1>
	</div>

<div id="show">

</div>

<div class="row">
	<div class="col-md-9">
		<div class="input-group input-group-lg">
			<span class="input-group-addon" id="sizing-addon1"></span> 
			<input id="input" name="pass" type="text" class="form-control" placeholder="新的密码"
				aria-describedby="sizing-addon1">
		</div>
	</div>
	<div class="col-md-2"></div>
	<div class="col-md-1">
		<button id="button" class="btn btn-primary">修改</button>
	</div>
</div>




</div>

<script>
$("#button").click(function() {
    console.log(111);
    $.ajax({
        type : 'post',
        url: "update" ,//url
        data: $('#input').serialize(),
        success : function() {
        	res = `<p class="bg-primary myin">修改成功</p>`;
            $('#show').html(res);
        }
    });
})
</script>

</body>
</html>
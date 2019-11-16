<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>

    
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<title>登录新闻发布系统</title>
	<script src="https://cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
	<script src="https://cdn.bootcss.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
	<script src="https://cdn.bootcss.com/datatables/1.10.13/js/jquery.dataTables.min.js"></script>
	<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css">
	<link rel="stylesheet" href="https://cdn.bootcss.com/datatables/1.10.13/css/jquery.dataTables.min.css">
	<style>
		* {
			margin: 0;
			padding: 0;
		}

		.back-ground {
			margin: 0;
			padding: 0;
			position: fixed;
			height: 100%;
			width: 100%;
			background: url(image/signup-background.jpg);
		}

		.my-position-login {
			position: absolute;
			top: 200px;
			right: 400px;
			width: 300px;
			height: 400px;
		}
		.mybtn {
			border-radius: 15px;
			padding-left: 110px;
			padding-right: 110px;
			text-align: center;
		}

		h1 {
			text-shadow: 2px 2px 8px #fff;
		}

		.find-password {
			display: block;
			margin-top: 5px;
			text-align: center;
		}
	</style>
	<script>
      function signup() {
    	  // TODO: 
      }
	</script>
</head>

<body>
<div class="back-ground">
	<div class="my-position-login">
		<div class="panel panel-default">
			<div class="panel-heading">
				<h3 class="panel-title">注册</h3>
			</div>
			<div class="panel-body">
				<form action="add" method="post">
					<div class="form-group">
						<label>用户名：</label>
						<input name="name" type="text" class="form-control" placeholder="User name">
					</div>
					<div class="form-group">
						<label>密码：</label>
						<input name="pass" type="password" class="form-control" placeholder="Password">
					</div>
					<div class="form-group">
						<label>确认密码：</label>
						<input name="pass1" type="password" class="form-control" placeholder="Password">
					</div>
					<hr>
					<button type="submit" class="btn btn-success mybtn">注册</button>
				</form>
			</div>
		</div>
	</div>
</div>
</body>
</html>
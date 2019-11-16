<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8" isELIgnored="false"%>
    
    <%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<title>Home</title>
	<script src="/news/js/jquery.js"></script>
	<script src="/news/js/bootstrap.min.js"></script>
	<link rel="stylesheet" href="/news/css/bootstrap.min.css">
	<style>
		.icon {
			width: 20px;
			height: 20px;
		}
	</style>
	<script>

	</script>
</head>

<body>

<div>
	<nav class="navbar navbar-default navbar-fixed-top navbar-inverse">
		<div class="container-fluid container">
			<div class="navbar-header">
				<button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
								data-target="#bs-example-navbar-collapse-1"
								aria-expanded="false">
					<span class="sr-only">Toggle navigation</span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</button>
				<a class="navbar-brand" href="#">新闻发布系统</a>
			</div>
			<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
				<ul class="nav navbar-nav">
					<li>
						<a class="menu" href="Main/index">首页</a>
					</li>
					<li class="dropdown">
						<a class="menu" href="Main/search" role="button" aria-haspopup="true" aria-expanded="false">新闻搜索

						</a>
					</li>

					<li class="dropdown">
						<a class="menu" href="Editor/index" role="button" aria-haspopup="true" aria-expanded="false">新建新闻</a>
					</li>
				</ul>

				<c:if test="${user==null}">
					<ul class="nav navbar-nav navbar-right">
					<li>
						<a href="Login/login">登录</span>
						</a>
					</li>
				</ul>
				</c:if>
				
				<c:if test="${user!=null }">
					<ul class="nav navbar-nav navbar-right">
					<li class="dropdown">
						<a href="#" class="dropdown-tooggle" data-toggle="dropdown" role="button">${user.name}<span class="caret"></span>
						</a>
						<ul class="dropdown-menu dropdown-round">
							<li><a class="menu" href="Main/info">信息修改</a></li>
							<li class="divider"></li>
							<li><a href="Login/logout">登出</a></li>
						</ul>
					</li>
				</ul>
				</c:if>
				
			</div>
		</div>
	</nav>
</div>

<div class="embed-responsive embed-responsive-16by9" style="margin-top: 50px">
  <iframe id="content" class="embed-responsive-item" width="100%" height="100%" src="Main/index"></iframe>
</div>

<footer>
	<div style="text-align:center; margin-top: 20px;">
		<p>All Copyright Reserved ©2019-07</p>
	</div>
</footer>

<script type="text/javascript">
	
    $(function () {
        $(".menu").on('click', function () {
            var url = $(this).attr('href');
            console.log("hello");
            $("#content").attr('src', url);
            return false;
        });
    });
</script>

</body>

</html>
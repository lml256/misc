<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<script src="/news/js/jquery.js"></script>
<script src="/news/js/bootstrap.min.js"></script>
<link rel="stylesheet" href="/news/css/bootstrap.min.css">
<title></title>

</head>

<body>

	<div class="container">
		<div class="page-header">
			<h1>查找新闻</h1>
		</div>

		<div class="search-item">
			<ul id="nav" class="nav nav-tabs">
				<li role="presentation" class="active" url="titleSearch"><a>标题查询</a></li>
				<li role="presentation" url="authorSearch"><a>作者查询</a></li>
				<li role="presentation" url="typeSearch"><a>类型查询</a></li>
			</ul>
		</div>
		<div id="router"></div>

	</div>

	<script>
		$("#nav li").click(function() {
			$('li').attr("class", "");
			$(this).attr("class", "active");
			var url = $(this).attr("url");
			$.ajax({
				url : url,
				type : 'get',
				success : function(res) {
					$('#router').html($(res));
				}
			});
		})

		$.ajax({
			url : 'titleSearch',
			type : 'get',
			success : function(res) {
				$('#router').html($(res));
			}
		});
	</script>

</body>

</html>
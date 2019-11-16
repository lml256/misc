<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8" isELIgnored="false"%>
	
	<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link
	href="http://cdn.bootcss.com/highlight.js/8.0/styles/monokai_sublime.min.css"
	rel="stylesheet">
<script src="/news/js/jquery.js"></script>
<script src="/news/js/bootstrap.min.js"></script>
<script src="https://cdn.bootcss.com/marked/0.7.0/marked.min.js"></script>
<link rel="stylesheet" href="/news/css/bootstrap.min.css">


</head>
<body>

	<div class="container">
		<div class="page-header">
			<h1 id="title"></h1>
		</div>

		<div id="show"></div>
	</div>
</body>
<script>
var id = ${id};
$.ajax({
    url : '../Editor/get?id=' + id,
    type : 'get',
    success : function(res) {
        console.log(res);
        $('#show').html(marked(res.body));
        $("#title").html(res.title);
    }
});
</script>
</html>
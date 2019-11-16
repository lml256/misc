<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8" isELIgnored="false" %>
	
	<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<script>
	function del(id){
		if(confirm("是否删除?"))
		{
			location.href="delete?id="+id;
		}
	}
	function edit(id){
		location.href="../Editor/update?id="+id;
	}
	</script>

<c:forEach items="${list}" var="r">
	<div class="news-item">
		<div class="row">
			<div class="col-md-9">
				<a href="show?id=${r.id}"><h1>${r.title}</h1></a>
			</div>
			<div class="col-md-3">
				<h4 style="color: #555">分类：${r.targetname}</h4>
			</div>
		</div>
		<div class="row">
			<div class="col-md-3">
				<h4>作者：${r.username}</h4>
			</div>
			<div class="col-md-6"></div>
			<div class="col-md-3">
				<c:if test="${user.id==r.userid || user.admin == 1}">
					<button class="btn btn-primary" onclick="javascript:edit(${r.id})">修改</button> &nbsp;&nbsp;
					<button class="btn btn-danger" onclick="javascript:del(${r.id})">删除</button>
				</c:if>
			</div>
		</div>
	</div>
	<hr>
</c:forEach>
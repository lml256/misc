<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8" isELIgnored="false"%>

	<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

 <h1>Type Search</h1>
 
<div class="container">
<div class="row">
<c:forEach items="${tlist }" var="r" varStatus="v">
	<div class="col-md-3"><a class="type" value="${r.id}"><h4>${r.name}</h4></a></div>
</c:forEach>
</div>
</div>

<div id="show"></div>

<script>
$(".type").click(function () {
    console.log("value="+$(this).attr("value"));
  $.ajax({
      type : 'post',
      url: "typeSearch" ,//url
      data: "value="+$(this).attr("value"),
      success : function(res) {
          $('#show').html($(res));
      }
  });
})
</script>

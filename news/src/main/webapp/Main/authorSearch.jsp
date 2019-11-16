<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>

	<h1>Author Search</h1>

	<div class="row">
		<div class="col-md-9">
			<div class="input-group input-group-lg">
				<span class="input-group-addon" id="sizing-addon1"></span> <input
					id="input" name="username" type="text" class="form-control" placeholder="作者"
					aria-describedby="sizing-addon1">
			</div>
		</div>
		<div class="col-md-2"></div>
		<div class="col-md-1">
			<button id="button" class="btn btn-primary">查询</button>
		</div>
	</div>
	
	
	<div id="show"></div>

<script>
    $("#button").click(function() {
        $.ajax({
            type : 'post',
            url: "authorSearch" ,//url
            data: $('#input').serialize(),
            success : function(res) {
                $('#show').html($(res));
            }
        });
    })
</script>
<html>
<head>
  <link href="//getbootstrap.com/dist/css/bootstrap.css" rel="stylesheet">
</head>
<body>
  <div class="container">
	<div class="row">
	  <div class="col-md-2"></div>

	  <div class="col-md-10">
		<h1>Bienvenido</h1>

		<form method="post" action="/signin" role="form">
		  <div class="form-group">
			<label for="signinInputEmail">Email</label>
			<input type="email"
				   name="username"
				   class="form-control"
				   id="signinInputEmail"
				   placeholder="Enter email">
		  </div>
		  <div class="form-group">
			<label for="signinInputPassword">Password</label>
			<input type="password"
				   name="password"
				   class="form-control"
				   id="signinInputPassword"
				   placeholder="Password">
		  </div>
		  <div class="checkbox">
			<label>
			  <input type="checkbox"> Mantener sesión
			</label>
		  </div>
		  <button type="submit" class="btn btn-primary">Ingresar</button>
		</form>
	  </div> <!-- col-md-10 -->

	</div> <!-- row -->
  </div> <!-- container -->

</body>
</html>

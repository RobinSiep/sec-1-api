<head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="static/css/bootstrap-material-design.min.css" >
    <link rel="stylesheet" href="static/css/ripples.min.css" >
    <link rel="stylesheet" href="static/css/main.css" >
    <link href="static/css/snackbar.min.css" rel="stylesheet">
    <script   src="https://code.jquery.com/jquery-3.1.1.min.js"   integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8="   crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
    <script src="static/js/material.min.js"></script>
    <script src="static/js/ripples.min.js"></script>
    <script src="static/js/main.js"></script>
    <script src="static/js/snackbar.min.js"></script>

    <script>
		$( document ).ready(function() 
		{
		    $(function() 
		    {
		        $.material.init();
		    });
		});    
	</script>
    <%block name="scripts">

    </%block>
</head>
<body>
	<div class="navbar navbar-inverse">
		<div class="container-fluid">
		    <div class="navbar-header">
		      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-inverse-collapse">
		        <span class="icon-bar"></span>
		        <span class="icon-bar"></span>
		        <span class="icon-bar"></span>
		      </button>
		      <a class="navbar-brand" href="/">Librator</a>
		    </div>
		    <%block name="nav_buttons">
		    </%block>
		</div>
	</div>
	<div class="col-lg-10 col-md-8 col-sm-10 col-xs-12 col-lg-offset-1 col-md-offset-2 col-sm-offset-1">
    	${self.body()}
    </div>

<body>


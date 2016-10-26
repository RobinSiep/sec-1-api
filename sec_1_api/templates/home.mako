<%inherit file="base.mako"/>
<%block name="scripts">
  <script src="static/js/logout.js"></script>
</%block>


<%block name="nav_buttons">
    <ul class="nav navbar-nav navbar-right">
        <li><a id="logout">logout</a></li>
    </ul>
</%block>




<%block name='pattern'>
	<div class="panel panel-default">
		<div class="panel-body">
			<p>Hieronder kan je je eigen tril patroon kiezen. een patroon bestaat uit 12 seconde. Voor iedere seconde kan worden gekozen of de vibrator trilt of niet.</p>
		</div>
	</div>


    <div class="panel panel-default">
        <div class="panel-heading">Tril patroon kiezen</div>
        <div class="panel-body">
	        <form id="pattern-form">
				<fieldset>
			      	% for i in range(12):
			        	<div class="alert col-md-1 ">
				            <div class="togglebutton col-md-offset-5">
				                <label>
				                	${i + 1} <br><br>
				                	<input id=${i} name=second_${i} value=1 type="checkbox" checkbox>
				              </label>
				            </div>
				        </div>
				    % endfor
			  	</fieldset>

			  	<input type="submit" class="btn btn-primary pull-right" value="Sla patroon op" />
			</form>
        </div>
    </div>
</%block>
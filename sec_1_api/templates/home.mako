<%inherit file="base.mako"/>
<%block name="scripts">
  <script src="static/js/logout.js"></script>
</%block>


<%block name="nav_buttons">
	<ul class="nav navbar-nav">
		% if admin:
	      <li><a href="firmware">firmware</a></li>
	    % endif
		<li><a href="device">Manage devices</a></li>
	</ul>
	<ul class="nav navbar-nav navbar-right">
        <li><a id="logout">logout</a></li>
    </ul>
</%block>




<%block name='pattern'>
	<div class="panel panel-default">
		<div class="panel-body">
			<p><h4>Here you can choose your vibration pattern. A pattern consists of 11 seconds. For every second you can choose if the vibrator vibrates or not</h4></p>
		</div>
	</div>


    <div class="panel panel-default">
        <div class="panel-heading">Tril patroon kiezen</div>
        <div class="panel-body">
	        <form id="pattern-form">
	        	<fieldset>
		        	<div class="form-group">
						<label for="device">Kies device</label>
							<select id="device" name='device_link_id' class="form-control">
							<option selected disabled>Choose Device..</option>
							% for device in devices:
					    		<option  value="${device.link_id}" pattern='${device.pattern}'>${device.name}</option>
					    	% endfor
						</select>
					</div>
				
					<div class="form-group">
						<div class="alert col-md-1 ">
				            <div class="togglebutton col-md-offset-5">
				                <label>
				                	On <br><br>
				                	<input name=on type="checkbox" value=1 checkbox>
				              </label>
				            </div>
				        </div>

				      	% for i in range(11):
				        	<div class="alert col-md-1 ">
					            <div class="togglebutton col-md-offset-5">
					                <label>
					                	${i + 1} <br><br>
					                	<input id=${i} name=second_${i} value=1 type="checkbox" checkbox>
					              </label>
					            </div>
					        </div>
					    % endfor
				    </div>

				    
			  	</fieldset>

			  	<input type="submit" class="btn btn-primary pull-right" value="Send" />
			</form>

        </div>
    </div>
</%block>

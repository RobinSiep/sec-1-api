<%inherit file="base.mako"/>
<%block name="scripts">
  <script src="static/js/logout.js"></script>
  <script src="static/js/device.js"></script>
  <script src='https://www.google.com/recaptcha/api.js'></script>
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
<form id="device-form" class="form-horizontal col-md-4 col-sg-12 col-md-offset-4">
  <fieldset>
    <div class="form-group">
      <div class="col-md-12">
        <input type="text" class="form-control" id="inputDeviceName" name="name" placeholder="Device Name">
        <p class="help-block">Give the device a custom name which you can use to identify the device in the application</p>
      </div>
    </div>
    <div class="form-group">
      <div class="col-md-12">
        <input type="text" class="form-control" id="inputDeviceIdentifier" name="link_id" placeholder="Pair ID">
         <p class="help-block">This identifier is show when you set up the device for the first time</p>
    </div>
  </fieldset>
  % if captcha:
      <div id="captcha"><div class="g-recaptcha" data-sitekey="6LdGPQoUAAAAAKtKfu_qAwr9rQWxapllFZWoLUtJ">
      </div></div>
   % endif
  <div class="form-group">
      <div>
        <input type="submit" class="btn btn-raised btn-primary col-md-12" value="Add New Device"/>
      </div>
    </div>
</form>
<table class="table table-striped table-hover">
<thead>
  <tr>
    <th>Added devices</th>
  </tr>
</thead>
<tbody>
  % for device in devices:
    <tr>
      <td><p>${device.name}</p></td>
      <td><button onclick="remove('${device.name}')" class="btn btn-raised btn-danger pull-right">Delete</button></td>
    </tr>
  % endfor
</tbody>
</table>
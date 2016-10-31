<%inherit file="base.mako"/>
<%block name="scripts">
  <script src="static/js/logout.js"></script>
  <script src="static/js/firmware.js"></script>
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
<form id="firmware-form" class="form-horizontal col-d-4 col-sg-12 col-md-offset-4">
  <fieldset>
    <div class="form-group">
      <div class="col-md-12">
        <input type="file" id="inputFirmware" name="firmware" placeholder="firmware"/>

        <p class="help-block">Upload a zip file containing the firmware</p>
      </div>
    </div>
  </fieldset>
  <div class="form-group">
      <div>
        <input id="upload" type="submit" class="btn btn-raised btn-primary col-md-12" value="Upload"/>
      </div>
    </div>
</form>
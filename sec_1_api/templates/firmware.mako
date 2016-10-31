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
<form id="firmware-form" class="form-horizontal col-md-4 col-sg-12 col-md-offset-4" enctype="multipart/form-data">
  <fieldset>
    <div class="form-group">
      <div class="col-md-12">

        <label for="inputFirmare">Click here to select a file to upload</label>
        <input type="file" id="inputFirmware" name="firmware" value=""/>
      </div>
    </div>
  </fieldset>
  <div class="form-group">
      <div>
        <input id="upload" type="submit" class="btn btn-raised btn-primary col-md-12" value="Upload"/>
      </div>
    </div>
</form>
<div class="col-md-12">
  <h3>Version log</h3>
  <table class="table table-striped table-hover">
  <thead>
    <tr>
      <th>Version</th>
      <th>Uploaded by</th>
      <th>Date (UTC)</th>
    </tr>
  </thead>
  <tbody>
    % for version in firmware:
      <tr>
        <td><p>${version.firmware_version}</p></td>
        <td><p>${version.uploader.username}</p></td>
        <td><p>${version.date_created}</p></td>
      </tr>
    % endfor
  </tbody>
  </table>
</div>
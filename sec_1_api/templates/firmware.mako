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
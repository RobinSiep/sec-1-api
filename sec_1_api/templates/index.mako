<%inherit file="base.mako"/>
<%block name="scripts">
  <script src="static/js/login.js"></script>
  <script src='https://www.google.com/recaptcha/api.js'></script>
</%block>
<form id="login-form" class="form-horizontal col-md-3 col-sg-12 center-absolute">
  <fieldset>
    <div class="form-group">
      <div class="col-md-12">
        <input type="text" class="form-control" id="inputUsername" name="username" placeholder="Username">
      </div>
    </div>
    <div class="form-group">
      <div class="col-md-12">
        <input type="password" class="form-control" id="inputPassword" name="password" placeholder="Password">
    </div>
    % if captcha:
      <div id="captcha"><div class="g-recaptcha" data-sitekey="6LdGPQoUAAAAAKtKfu_qAwr9rQWxapllFZWoLUtJ"></div></div>
    % endif
    <div class="form-group">
      <div>
        <button class="btn btn-danger" onclick="location.href='recover';">Forgot password?</button>
        <input type="submit" class="btn btn-primary pull-right" value="Sign in" />
        <button class="btn btn-default col-md-12" onclick="location.href='signup';">No account? Sign up instead</button>
      </div>
    </div>
  </fieldset>
</form>

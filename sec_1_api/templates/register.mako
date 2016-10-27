<%inherit file="base.mako"/>
<%block name="scripts">
  <script src="static/js/signup.js"></script>
  <script src='https://www.google.com/recaptcha/api.js'></script>
</%block>
<div class="well col-md-6 col-md-offset-3">
  <form id="signup-form" class="form-horizontal">
    <fieldset>
      <div class="form-group">
        <label for="inputUsername" class="col-md-2 control-label">Username</label>

        <div class="col-md-10">
          <input type="text" class="form-control" id="inputUsername" name="username" placeholder="Username">
        </div>
      </div>
      <div class="form-group">
        <label for="inputEmail" class="col-md-2 control-label">Email</label>

        <div class="col-md-10">
          <input type="email" class="form-control" id="inputEmail" name="email" placeholder="Email">
          <p class="help-block">Email is optional and will only be used when recovering the account. Keep in mind that the account can't be recovered without an email if you happen
          to forget your password.</p>
        </div>
      </div>
      <div class="form-group">
        <label for="inputPassword" class="col-md-2 control-label">Password</label>

        <div class="col-md-10">
          <input type="password" class="form-control" id="inputPassword" name="password" placeholder="Password">
          <p class="help-block">A minimum of 8 characters need to be used. The password needs to contain at least 1 letter and 1 number.</p>
        </div>
      </div>
      <div class="form-group">
        <label for="passwordRepeat" class="col-md-2 control-label">Password (repeat)</label>

        <div class="col-md-10">
          <input type="password" class="form-control" id="passwordRepeat" name="password_confirm" placeholder="Password (repeat)">
          <p class="help-block">Needs to be the same as the password filled in above.</p>
        </div>
      </div>
      <div class="form-group">
      <div id="captcha"><div class="g-recaptcha pull-right" data-sitekey="6LdGPQoUAAAAAKtKfu_qAwr9rQWxapllFZWoLUtJ"></div></div>
        <div class="col-md-12">
          <input type="submit" class="btn btn-primary pull-right" value="Sign up"/>
        </div>
      </div>
    </fieldset>
  </form>
</div>
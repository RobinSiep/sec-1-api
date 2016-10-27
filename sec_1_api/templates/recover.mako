<%inherit file="base.mako"/>
<%block name="scripts">
  <script src="static/js/recover.js"></script>
  <script src='https://www.google.com/recaptcha/api.js'></script>
</%block>
<div class="col-md-3 col-sg-12 center-absolute">
	<form id="recover-email-form" class="form-horizontal">
	% if send_captcha or recovery_captcha:
	     <div id="captcha"><div class="g-recaptcha" data-sitekey="6LdGPQoUAAAAAKtKfu_qAwr9rQWxapllFZWoLUtJ"></div></div>
	% endif
		<fieldset>
		    <div class="form-group">
		      <div class="col-md-10">
		        <input type="email" class="form-control" id="inputEmail" name="email" placeholder="Email">
		      </div>
		    </div>
		    
		  	<div class="form-group">
		    	<div>
		        	<input type="submit" class="btn btn-raised btn-primary col-md-10 col-md-offset-1" value="Send recovery code" />
		    	</div>
			</div>
	  	</fieldset>
	</form>
	<form id="recover-code-form" class="form-horizontal" style="display: none">
		<fieldset>
		    <div class="form-group">
	        <div class="col-md-10">
	          <input type="password" class="form-control" id="inputPassword" name="password" placeholder="New password">
	          <p class="help-block">A minimum of 8 characters need to be used. The password needs to contain at least 1 letter and 1 number.</p>
	        </div>
	      </div>
	      <div class="form-group">
	        <div class="col-md-10">
	          <input type="password" class="form-control" id="passwordRepeat" name="password_confirm" placeholder="New password (repeat)">
	          <p class="help-block">Needs to be the same as the password filled in above.</p>
	        </div>
	      </div>
	       <div class="form-group">
		      <div class="col-md-10">
		        <input type="text" class="form-control" id="inputCode" name="recovery_code" placeholder="Recovery code">
		      </div>
		   </div>
		  	<div class="form-group">
		    	<div>
		        	<input type="submit" class="btn btn-raised btn-primary col-md-10 col-md-offset-1" value="Recover account" />
		        	<button id="stepBack" class="btn btn-raised btn-default col-md-10 col-md-offset-1">Back to previous step </button>
		    	</div>
			</div>
	  	</fieldset>
	</form>
</div>
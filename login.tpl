<!DOCTYPE html>
<title>Login</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<style type="text/css">
<!-- 
body {
   width:700px;
   margin:auto;
   background-color:#FFFDF0;
}
form {
   width:500px;
   margin-top:5em;
}
p {
   text-align:right;
}

input {
   font-size:2em;
}
-->
</style>

<script>
"use strict"

function setCookie(name,value,days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}

function setPass() {
	setCookie("username", document.forms["frm1"]["username"].value, 364);
	setCookie("password", document.forms["frm1"]["password"].value, 364);
}
</script>

<form id="frm1">
  <p><input name="username" type="text" placeholder="Username">
  <p><input name="password" type="password" placeholder="Password">
  <p><input type="submit" onClick=setPass()>
</form>

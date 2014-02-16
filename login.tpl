<!DOCTYPE html>

<!-- 
login.tpl - Login form for tinypass.pl.

It uses the float label form implementation by Aaron Barker (http://codepen.io/aaronbarker/pen/tIprm)

I chose to use Zepto.js (http://zeptojs.com/) instead of jQuery 2.X, since I was unwilling to add 90kb of bloat just for a
dumb CSS animation. Nobody using IE9 or worse will see it, but that's why they call it progressive enhancement.

Written by bbot@bbot.org
This is free and unencumbered software released into the public domain.
-->

<title>Login</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<style type="text/css">
<!-- 
body{width:700px;background-color:#FFFDF0;font:2em sans-serif;-webkit-backface-visibility:hidden;margin:auto;padding:20px;}form{width:500px;margin-top:5em;}input{font:1em sans-serif;}p{line-height:2.1em;}.field--wrapper{position:relative;margin-bottom:20px;}label{position:absolute;top:-13px;left:0;color:#aaa;transition:all .1s linear;opacity:0;font-family:sans-serif;}label.on{color:#4481C4;}label.show{top:-1.2em;opacity:1;}
-->
</style>

<form id="frm1">
  <p class="field--wrapper"><label for="username">Username</label><input name="username" type="text" placeholder="Username">
  <p class="field--wrapper"><label for="password">Password</label><input name="password" type="password" placeholder="Password">
  <!--Little funny that I end up repeating the name of each field four times, but there's no elegant way to DRY here, oh well.-->
  <p><input type="button" value="Submit" onClick=setPass()>
</form>

<!--This holds all the float label magic.-->
<script async src=float-label.js></script>

<!--And this is the cookie handling code.-->
<script async>
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
	setCookie("username", document.forms["frm1"]["username"].value);
	setCookie("password", document.forms["frm1"]["password"].value);
	document.location.reload(true)
}
</script>


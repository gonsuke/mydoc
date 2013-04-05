# -*- coding: utf-8 -*-

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja" dir="ltr">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>${attributes['db']}</title>
<style type=text/css>
table	{
	border-collapse: collapse;	border-spacing: 0;
}
body {
	font-family: verdana,"ヒラギノ角ゴ Pro W3","Hiragino Kaku Gothic Pro",Osaka,"ＭＳ Ｐゴシック","MS PGothic",Sans-Serif;
	color: #333;
	font-size: 75%;
	line-height: 150%;
}
html>/**/body {
	font-size: 12px;
}
div.main	{
	width: 980px;
}
h3	{
	font-size: 133.3%;
	margin-bottom: 5px;
}
table	{
	border-collapse: collapse;	border-spacing: 0;
	width: 100%;
	margin-bottom: 30px;
}
th, td	{
	padding: 10px 10px;
	color: #1D5C79;
}
.bluetable th	{
	background: #A0C9DB;
	border-top: 2px solid #1D5C79;
	border-bottom: 1px solid #FFF;
	text-align: left; 
}
.bluetable td	{
	background: #E5F2F8;
	border-bottom: 1px solid #FFF;
	text-align: left; 
}
a:link
{
	color:#215dc6;
	background-color:inherit;
	text-decoration:none;
}
a:active
{
	color:#215dc6;
	background-color:#CCDDEE;
	text-decoration:none;
}
a:visited
{
	color:#a63d21;
	background-color:inherit;
	text-decoration:none;
}
a:hover
{
	color:#215dc6;
	background-color:#CCDDEE;
	text-decoration:underline;
}
</style>
</head>

<body>
<h1>Data Dictionary for: ${attributes['db']}</h1>

<img src='./erd.png'> </img>

<ul class="simple">

<% index = 1 %>
% for t in attributes['tables'].iterkeys():
  <li><a class="reference" href="#${t}" id="id${index}" name="id1">${t}</a></li>
  <% index += 1 %>
% endfor

</ul>
<div class="main">

<% index = 1 %>
% for t, t_content in attributes['tables'].iteritems():
    <h3><a href="#id${index}" id="${t}">${t}</a></h3>
<ul class="simple">

	% for comment in t_content['comments']:
	<li> ${comment} </li>
	% endfor

</ul>
    <table class="bluetable">
    <thead>
    <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Null</th>
    <th>Key</th>
    <th>Default</th>
    <th>Extra</th>
    <th>Comment</th>
    </tr>
    </thead>
    <tbody>

	% for c, c_content in t_content['columns'].iteritems():
       <tr>
	   <td>${c}</td>
	   <td>${c_content['type']}</td>
	   <td>${c_content['null']}</td>
	   <td>${c_content['key']}</td>
	   <td>${c_content['default']}</td>
	   <td>${c_content['extra']}</td>
	   <td>${c_content['comment']}</td>
       </tr>
	% endfor

    </tbody>
    </table>
  <% index += 1 %>
% endfor

</div>
</body>
</html>

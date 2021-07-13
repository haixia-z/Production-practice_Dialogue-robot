<?php
session_start();
require 'dadb.php';
if (empty($_SESSION["username"])) {
    header("Location:login.php");
    exit;
}else{
    $user_name=$_SESSION["username"];
    //var_dump($user_name);
    $sql="select *from User where user_name='$user_name'";
    $res=$conn->query($sql);
    if ($res) {
        $row=$res->fetch_assoc();
        $user_phone=$row["user_phone"];
        $user_pic=$row["user_pic"];
        $user_gender=$row["user_gender"];
        $user_site=$row["user_site"];
        $user_level=$row["user_level"];
    }
 }
?>
<!DOCTYPE html>
<html>
<head>
	<title>对话机器人管理</title>
	<meta charset="utf-8">
	<link rel="stylesheet" type="text/css" href="index.css">
	<!-- bootstrap框架，联网 -->
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
</head>
<body>
<div class="allBox">
<!-- 左侧导航 -->
<nav class="leftNav">
	<div>
		<ul class="navBox">
			<li class="navTitle">
				<div class="titleBox">
					<a href="index.php" class="title">对话机器人管理</a>
				</div>
			</li>
			<li class="navHeader">
				<div class="headerBox">
					<a href="index.php" class="header">
						添加问题和答案
					</a>
				</div>
			</li>
			<!-- <li class="navHeader">
				<div class="headerBox">
					<a href="operator.php" class="header">
						操作日志
					</a>
				</div>
			</li> -->
		</ul>
	</div>
</nav>
<!-- 右侧导航 -->
<div class="topWrapper">
<nav class="rightNav">
	<div class="welcomBox">
		<div class="indent">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="24" height="24"><path d="M0 84V44c0-8.837 7.163-16 16-16h416c8.837 0 16 7.163 16 16v40c0 8.837-7.163 16-16 16H16c-8.837 0-16-7.163-16-16zm176 144h256c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H176c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16zM16 484h416c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H16c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16zm160-128h256c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H176c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16zm-52.687-111.313l-96-95.984C17.266 138.652 0 145.776 0 160.016v191.975c0 14.329 17.325 21.304 27.313 11.313l96-95.992c6.249-6.247 6.249-16.377 0-22.625z" style="fill: rgba(146, 146, 146)"></path></svg>
		</div>
		<span>
				欢迎进入对话机器人管理平台！
		</span>
	</div>
	<div>
		<a href="/jk-museum/UserManage/userCenter.php"><img src="/jk-museum/UserManage/images/<?=$user_pic?>" class="userAvater"></a>
		<span><a href="quit.php" class="Astyle">退出</a></span>
	</div>
</nav>
<div>
	<form class="form-horizontal" action="addQA.php" method="post">
	  <div class="form-group">
	    <label for="inputEmail3" class="col-sm-2 control-label">问题</label>
	    <div class="col-sm-10">
	      <input class="form-control" id="inputEmail3" placeholder="在此处输入问题" name="question">
	    </div>
	  </div>
	  <div class="form-group">
	    <label for="inputPassword3" class="col-sm-2 control-label" >答案</label>
	    <div class="col-sm-10">
	      <input class="form-control" id="inputPassword3" placeholder="在此处输入答案"name="answer">
	    </div>
	  </div>
	  <div class="form-group">
	    <div class="col-sm-offset-2 col-sm-10">
	      <button type="submit" class="btn btn-default">添加</button>
	    </div>
	  </div>
	</form>
</div>
</div>
</body>
</html>
<?php
session_start();
if (empty($_SESSION["username"])) {
	header("Location: login.php");
  exit;
 }
require'dadb.php';

// 操作日志
$username=$_SESSION["username"];
header("Content-type: text/html; charset=utf-8"); 
date_default_timezone_set('Asia/Shanghai'); 
$chinatime = date('Y-m-d H:i:s');
$fileName=date("Ymd").".log";
$RootDir = $_SERVER['DOCUMENT_ROOT']; 
$filePath="$RootDir/FAQrobotManage/operatorManage/".$fileName;
// var_dump($filePath);
if (!file_exists($filePath)) {
    $myfile=fopen("$filePath", "w");
}
$max_size = 500000;
 error_reporting(0);//关闭所有的错误信息，不会显示，如果清除掉，会将错误的日志写入到log中
ini_set('log_errors','on');
error_log('示例的错误信息');

$question=$_POST["question"];
$answer=$_POST["answer"];
// var_dump($question);
// var_dump($answer);
$flag=1;
if (empty($question)||empty($answer)) {
	 // echo '<script>alert("问题和答案不能为空！");history.go(-1);</script>';
	$falg=0;
	exit();
}

// var_dump($flag);

if ($flag) {
		$sql="INSERT INTO q_a(question, answer)VALUES ('$question','$answer')";
		$res=$conn->query($sql);
		// var_dump($res);
		if ($res) {
			ini_set('error_log',"$filePath");
            error_log($username." 添加问题"." ip地址:".$_SERVER['REMOTE_ADDR']."添加问题:".$user_name."成功 ".date("Y-m-d H:i:s"));
            
			echo '<script>alert("增添问题成功！");window.location="index.php"</script>';
		}else{
			ini_set('error_log',"$filePath");
            error_log($username." 添加问题"." ip地址:".$_SERVER['REMOTE_ADDR']."添加问题:".$user_name."失败 ".date("Y-m-d H:i:s"));
			echo '<script>alert("增添问题失败");</script>';
		}
	}

?>
<?php

$host='localhost';
$myusername='root';
$mypassword='chear';
$dbname='dialogue_robot';
$conn = new mysqli($host,$myusername,$mypassword,$dbname);

if($conn->connect_error){
	die("连接错误：".mysqli_connect_error());
}

$conn->query("SET NAMES 'UTF8'");
?>
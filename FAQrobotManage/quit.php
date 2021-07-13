<?php
session_start();
header("location:login.php");
setcookie("username","",time()-3600);
session_destroy();
?>

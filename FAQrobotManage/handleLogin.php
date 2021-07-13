<?php
session_start();
require_once ('dadb.php');

header("Content-type: text/html; charset=utf-8"); 
date_default_timezone_set('Asia/Shanghai'); 
$chinatime = date('Y-m-d H:i:s');
$fileName=date("Ymd").".log";
$RootDir = $_SERVER['DOCUMENT_ROOT']; 
$filePath="$RootDir/FAQrobotManage/operatorManage/".$fileName;
if (!file_exists($filePath)) {
    $myfile=fopen("$filePath", "w");
}
$max_size = 500000;
 // error_reporting(0);//关闭所有的错误信息，不会显示，如果清除掉，会将错误的日志写入到log中
// ini_set('log_errors','on');
error_log('示例的错误信息');

    $logInfo='';
    //$logInfo='<span style="color: red;">Please enter username</span>';
    $logIndex = 1;
    $time=(int)date("H");


    $username=$_POST['Username'] ?? '';
    $password=$_POST['Password'] ?? '';
    // var_dump($username);
    $level;
    //正则识别
// 1.允许输入字符：数字(0-9)、字母(a-z和A-Z)、汉字、下划线(_)、圆点(.)和空格；
//2、姓名中间允许有空格；
//3、下划线、圆点和空格均为英文状态输入法下的字符；
//4、姓名前后不允许输入下划线、圆点、空格和特殊字符
    $user_pattern='/^[a-zA-Z0-9\x{4e00}-\x{9fa5}]+$|^[a-zA-Z0-9\x{4e00}-\x{9fa5}][a-zA-Z0-9_\s\ \x{4e00}-\x{9fa5}\.]*[a-zA-Z0-9\x{4e00}-\x{9fa5}]+$/u';
    $pwd_pattern='/^\w{8,16}$/S';

    if(!empty($username)) {
        if (preg_match($user_pattern, $username)) {
            $logIndex = 2;
        }else{
            $logIndex = 0;
        }
    }else{
        echo'<script>alert("用户名为空");history.go(-1);</script>';
    }

    if(!empty($password)){
        if(preg_match($pwd_pattern,$password)){
            $logIndex = 2;
        }else{
            $logIndex = 0;
        }
    }else{
        echo'<script>alert("密码为空");history.go(-1);</script>';
    }

    if($logIndex=0){
        $logInfo = '<span style="color: red; ">Failed</span>';
    }else if($logIndex=2){
        $logInfo = '';
    }else{
        $logInfo = '<span style="color: green; ">Succeed</span>';
    }
    $conn_index=1;
// var_dump($conn_index);
    if($conn_index>0){
        // $realpassword=md5($password);
        $sql = "SELECT user_name,user_password,user_level FROM `User` where user_name='$username' and user_password='$password'";
        $result = $conn->query($sql);


        $logIndex=0;
         // var_dump($result);
        if ($result) {
            $row = $result->fetch_assoc();
            // var_dump($row);
                if ($row["user_name"] == $username && $row["user_password"] == $password && $row["user_level"] >= 2) {
                    $level=$row["user_level"];
                    $logIndex = 1;
                    $_SESSION['username']=$username;
                    $_SESSION['level']=$level;
                    
                    ini_set('error_log',"$filePath");
                    error_log($username." 登录"." ip地址:".$_SERVER['REMOTE_ADDR']."登录成功 ".date("Y-m-d H:i:s"));
                    //var_dump($filePath);
                    //var_dump('error_log');
                    echo'<script>alert("登录成功！");window.location="index.php"</script>';
                
            }
        if(!empty($username)&&!empty($password)&&$logIndex==0)
                echo'<script>alert("当前用户权限非管理员");history.go(-1);</script>';
        }else{
            ini_set('error_log',"$filePath");
            error_log($username." 登录"." ip地址:".$_SERVER['REMOTE_ADDR']."登录失败 ".date("Y-m-d H:i:s"));
             echo'<script>alert("登录失败！");history.go(-1);</script>';
            // 
        }

    }
?>
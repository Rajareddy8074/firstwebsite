<?php
session_start();
$id=$_SESSION['name'];
$l= $_POST['dname'];
$servername = "localhost";
$password = "";
$dbname = "raja";
$conn = mysqli_connect($servername, 'root', $password, $dbname);
$sql = "SELECT * FROM likes where uname='$id' and name='$l' and action='dislike'";
$result = mysqli_query($conn,$sql);
if(mysqli_num_rows($result)==0){
    $result = mysqli_query($conn,"INSERT INTO `likes`(`uname`, `name`, `action`) VALUES ('$id','$l','dislike')");
}
$sql = "SELECT * FROM likes where uname='$id' and name='$l' and action='like'";
$result = mysqli_query($conn,$sql);
if(mysqli_num_rows($result)){
    $result = mysqli_query($conn,"delete from likes Where uname='$id' and name='$l' and action='like'");  
}
header("Location:index.php");
?>
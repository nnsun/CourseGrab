<?php
    $email = $_POST['email'];
    $number = $_POST['course_number'];
    if(empty($email) || empty($number))
        {//show the form
        $message = 'Fill in areas in red!';
        $aClass = 'errorClass';
    }
    $cvsData = $email . "," . $number . "\n";
    $fp = fopen("../scripts/obey.csv","a");
    if($fp){
     fwrite($fp,$cvsData); // Write information to the file
     fclose($fp); // Close the file
    }
    if(processing == success) {
      header("Location:success.html");
      exit();
    }
?>
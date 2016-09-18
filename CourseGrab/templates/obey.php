<html>
  <head>
    <title>Thanks! <br> We will send an email to ["email"] when the course is open.</title>
  </head>
  <?php
    header( 'Location: success.html' )
    $data = array("course_number" . ',' . "email" . '\n');
    $cr;

    $fp = fopen("../scripts/ledger.csv","w");
    foreach ($data as $fields){
      fputcsv($fp, $fields);
    }
    fclose($fp);
  ?>
</html>
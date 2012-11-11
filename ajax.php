<?php
$vid = $_REQUEST['vid'];
$file = 'assets/'.$vid.'/'.$vid.'_slices.json';
if (file_exists($file)) {
  $i = $_REQUEST['i'];
    header('Content-Type: application/javascript');
    ob_clean();
    flush();
    echo 'vid_slices['.$i.'] = ';
    readfile($file);
    echo ';';
    echo 'vids_loaded++;';
    exit;
}
?>

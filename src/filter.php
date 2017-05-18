<?php

require_once __DIR__.'/menu.php';

if ($_POST['btnSubmit']) {
	$cmd = __DIR__.'/../emeocv/Debug/emeocv -i '.__DIR__.'/../cache -A '.__DIR__.'/../data';
	echo $cmd, '<br />', PHP_EOL;
	echo '<pre style="background: gray">';
	passthru($cmd);
	echo '</pre>';
}
?>

<form action="filter.php" method="post">
	<input type="submit" name="btnSubmit" value="Check" />
</form>

<img src="../data/source.png" /><br />
<img src="../data/filteredContours.png" /><br />

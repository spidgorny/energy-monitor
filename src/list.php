<?php

$files = glob(__DIR__.'/../cache/*.png');
foreach ($files as $file) {
	echo '<img src="../cache/'.basename($file).'" width="128" />', PHP_EOL;
}

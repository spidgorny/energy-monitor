<?php

require_once __DIR__.'/bootstrap.php';

function __($a) {
	return $a;
}

$config = Config::getInstance();
echo Index::getInstance(true, $config)->render();

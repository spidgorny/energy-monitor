<?php

require_once __DIR__.'/bootstrap.php';

function __($a) {
	return $a;
}

echo Index::getInstance(1)->render();

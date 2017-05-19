<?php

$filename = __DIR__.'/load.rrd';

$begin = new DateTime( '2017-01-01' );
$end = new DateTime( '2017-12-31' );

$interval = DateInterval::createFromDateString('1 second');
$period = new DatePeriod($begin, $interval, $end);

/** @var DateTime $time */
foreach ($period as $time) {
	if (!($time->getTimestamp() % 10000)) {
		echo $time->format('Y-m-d H:i'), PHP_EOL;
	}
	$ok = rrd_update($filename, [$time->getTimestamp() . ':' . round(rand(0, 255))]);
}

function rrd_update($filename, array $time_value_array) {
	$path = 'c:/wamp/vdrive/.sys/rrdtool.exe update';
	$cmd = $path . ' ' . escapeshellarg($filename) . ' ' . escapeshellarg($time_value_array[0]);
	echo $cmd, PHP_EOL;
	return exec($cmd);
}

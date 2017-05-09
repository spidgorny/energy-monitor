<?php

date_default_timezone_set('Europe/Berlin');

//$filename = __DIR__.'/load.rrd';
$filename = __DIR__.'/speed.rrd';

$info = rrd_info($filename);

print_r($info);
$step = $info['step'];
$first = rrd_first($filename);
$last = rrd_last($filename);
echo 'First: ', $first, ' ', date('Y-m-d H:i', $first), PHP_EOL;
echo 'Last: ', $last, ' ', date('Y-m-d H:i', $last), PHP_EOL;

$data = rrd_fetch($filename, [
//	'-a',
	"AVERAGE",
//	"--resolution", $step,
	'-s',
	$first,
	'-e',
	$last,
]);

print_r($data);

if (0) {
	$xport = rrd_xport([
		'-s',
		$first,
		'-e',
		$last,
		'--step',
		$step,
		'--json',
		'DEF:speed=' . $filename . ':42:AVERAGE',
		'XPORT:xx:"out bytes"'
	]);
}

$ok = rrd_graph(__DIR__ . "/speed.png", [
	"--start", $first,
	"--end", $last,
	"--vertical-label", "m/s",
	"DEF:myspeed=$filename:speed:AVERAGE",
	"CDEF:realspeed=myspeed,1000,*",
	"LINE2:realspeed#FF0000"
]);
echo 'Graph: ', $ok ? 'ok' : 'fail', PHP_EOL;

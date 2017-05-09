<?php

date_default_timezone_set('Europe/Berlin');

$rrdFile = dirname(__FILE__) . "/speed.rrd";

if (!file_exists($rrdFile)) {
	rrd_create($rrdFile,
		array(
			"--start", time(),
			"DS:speed:COUNTER:600:U:U",
			"RRA:AVERAGE:0.5:1:24",
			"RRA:AVERAGE:0.5:6:10"
		)
	);
}

$info = rrd_info($rrdFile);
print_r($info);
$last_ds = $info['ds[speed].last_ds'];

$ok = rrd_update($rrdFile,
	array(
//		"920804700:12345",
//		"920805000:12357"
		time().':'.($last_ds+1)
	)
);

echo $ok ? 'ok' : 'fail', PHP_EOL;

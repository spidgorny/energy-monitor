<?php

$rrdFile = "/home/ubuntu/emeocv/speed.rrd";

$updater = new RRDUpdater($rrdFile);
$updater->update(array("speed" => "12411"));

foreach (range(0, 100) as $x) {
	$speed = rand(0, 250);
	echo $x, "\t", $speed, PHP_EOL;
	$updater->update(["speed" => $speed]);
	sleep(1);
}

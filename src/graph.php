<?php

$rrdFile = "/home/ubuntu/emeocv/speed.rrd";
$outputPngFile = dirname(__FILE__) . "/speed.png";

$graphObj = new RRDGraph($outputPngFile);
$graphObj->setOptions(
	array(
		"--start" => "920804400",
		"--end" => 920808000,
		"--vertical-label" => "m/s",
		"DEF:myspeed=$rrdFile:speed:AVERAGE",
		"CDEF:realspeed=myspeed,1000,*",
		"LINE2:realspeed#FF0000"
	)
);
$graphObj->save();

<?php

$filename = __DIR__.'/load.rrd';

$ok = rrd_update($filename, [time().':'.round(rand(0, 255))]);

echo $ok ? 'ok' : 'fail', PHP_EOL;


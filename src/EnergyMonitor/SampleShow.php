<?php
/**
 * Created by PhpStorm.
 * User: DEPIDSVY
 * Date: 24.05.2017
 * Time: 11:29
 */

namespace EnergyMonitor;


use EnergyMonitor\OpenCV\Sample;

class SampleShow extends AppController
{

	function imgAction() {
		$s = new Sample([], 0, 0);
		$s->render();
	}

}

<?php
/**
 * Created by PhpStorm.
 * User: DEPIDSVY
 * Date: 22.05.2017
 * Time: 16:03
 */

namespace EnergyMonitor;


use Symfony\Component\Yaml\Yaml;

class CheckTraining extends AppController
{

	function render() {
		$file = __DIR__.'/../../data/training.yml';
		$data = Yaml::parse(file_get_contents($file));
		return sizeof($data);
	}

}

<?php
/**
 * Created by PhpStorm.
 * User: DEPIDSVY
 * Date: 22.05.2017
 * Time: 16:03
 */

namespace EnergyMonitor;


use EnergyMonitor\OpenCV\Matrix;
use EnergyMonitor\OpenCV\Sample;
use Symfony\Component\Yaml\Exception\ParseException;
use Symfony\Component\Yaml\Yaml;

class CheckTrainingHollow extends AppController
{

	function render() {
		$content = [];
		$files = glob(__DIR__.'/../../python/training/*.*');
		foreach ($files as $file) {
			$content[] = '<h5>'.basename($file).'</h5>';
			$yaml = file_get_contents($file);
			$yaml = str_replace('!!opencv-matrix', '!opencv-matrix', $yaml);
			$data = Yaml::parse($yaml, Yaml::PARSE_CUSTOM_TAGS);

			$digits = [];
			foreach ($data as $name => $info) {
				if (str_startsWith($name, 'digit')) {
					$digits[] = $info;
				}
			}
			$numbers = $data['numbers'];
			$content[] = 'numbers: ' . implode(', ', $numbers) . BR;

			foreach ($digits as $i => $d) {
				$matrix = new OpenCV\Matrix($d->getValue());
//				$content[] = 'rows: ' . $matrix->getRows() . BR;
//				$content[] = 'cols: ' . $matrix->getCols() . BR;
				$content[] = $this->renderSamples($matrix, $numbers[$i]);
			}
		}
		return $content;
	}

	function renderSamples(Matrix $matrix, $digit)
	{
		$content = [];
		$data = $matrix->getData();
		$sample = new Sample($data, $matrix->getCols(), $matrix->getRows());
		$content[] = '<img src="' . $sample->getImagePath() . '" />' . '&nbsp;';

		$content[] = '<big>' . $digit . '</big>' . ' ';
		return $content;
	}

}

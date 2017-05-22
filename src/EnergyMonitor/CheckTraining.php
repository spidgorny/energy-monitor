<?php
/**
 * Created by PhpStorm.
 * User: DEPIDSVY
 * Date: 22.05.2017
 * Time: 16:03
 */

namespace EnergyMonitor;


use EnergyMonitor\OpenCV\Matrix;
use Symfony\Component\Yaml\Exception\ParseException;
use Symfony\Component\Yaml\Yaml;

class CheckTraining extends AppController
{

	function render() {
		$content = [];
		$file = __DIR__.'/../../data/training.yml';
		try {
			$yaml = file_get_contents($file);
			$yaml = str_replace('!!opencv-matrix', '!opencv-matrix', $yaml);
			$data = Yaml::parse($yaml, Yaml::PARSE_CUSTOM_TAGS);
//			\Debug::peek($data);

			list($source, $digits) = [$data['samples'], $data['responses']];

			$matrix = new OpenCV\Matrix($source->getValue());
			$content[] = 'rows: '.$matrix->getRows().BR;
			$content[] = 'cols: '.$matrix->getCols().BR;

			$sampleData = $matrix->getOne(0);
			foreach (range(0, 9) as $l) {
				$line = array_slice($sampleData, $l * 10, 10);
				$content[] = implode(', ', $line) . BR;
			}

			$digitMat = new OpenCV\Matrix($digits->getValue());

			$content[] = $this->renderSamples($matrix, $digitMat);
		} catch (ParseException $e) {
			$content = get_class($e);
		}
		return $content;
	}

	function renderSamples(Matrix $matrix, Matrix $digitMat)
	{
		$content = [];
		foreach (range(0, 10) as $index) {
			$sample = $matrix->getSample($index);
			$content[] = '<img src="' . $sample->getImagePath() . '" />' . BR;

			$digit = $digitMat->getOne($index);
			$content[] = '<big>' . $digit[0] . '</big>' . BR;
		}
		return $content;
	}

}

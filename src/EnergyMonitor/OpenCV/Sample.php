<?php

namespace EnergyMonitor\OpenCV;


class Sample {

	protected $rows = 10;

	protected $cols = 10;

	/**
	 * @var int[]
	 */
	protected $data;

	public $layout = null;

	function __construct(array $data = NULL, $width, $height)
	{
		if ($data) {
			assert(sizeof($data) == $width * $height);
		}
		$this->data = $data;
		$this->cols = $width;
		$this->rows = $height;
	}

	function getImagePath() {
		return 'SampleShow?'.http_build_query([
			'action' => 'img',
			'width' => $this->cols,
			'height' => $this->rows,
			'data' => base64_encode(gzcompress(
//				implode(',', $this->data)
				pack("c*", ...$this->data)
			)),
		]);
	}

	function render() {
		$request = \Request::getInstance();
		$data = $request->getBase64('data');
//		$this->data = trimExplode(',', $data);
		$this->data = unpack('C*', gzuncompress($data));
//		debug($_REQUEST['data'], strlen($data), sizeof($this->data));
		$this->rows = $request->getInt('height');
		$this->cols = $request->getInt('width');

		//pre_print_r($this->cols, $this->rows, strlen($data), sizeof($this->data));
		assert(sizeof($this->data) == $this->rows*$this->cols);
//		flush();
		if (!headers_sent()) {
			$this->imgAction(1);
		} else {
			$this->spellSample();
			exit;
		}
	}

	function imgAction($t = 1) {
		$img = imagecreatetruecolor($this->cols * $t,
			$this->rows * $t);
		reset($this->data);
		foreach (range(0, $this->rows-1) as $r) {
			foreach (range(0, $this->cols-1) as $c) {
				$value = current($this->data);
				$c1 = imagecolorallocate($img, $value, $value, $value);
				imagefilledrectangle($img, $c*$t, $r*$t,
					$c*$t+$t, $r*$t+$t, $c1);

				next($this->data);
			}
		}

		\Request::getInstance()->setCacheable(60*60*24*356);
		header('Content-Type: image/png');
		imagepng($img);
		exit;
	}

	/**
	 */
	private function spellSample() {
		echo '<pre>';
		reset($this->data);
		foreach (range(0, $this->rows-1) as $r) {
			foreach (range(0, $this->cols-1) as $c) {
				$value = current($this->data);
				echo $value ? 1 : '-', '';
				next($this->data);
			}
			echo PHP_EOL;
		}
		echo '</pre>';
	}

}

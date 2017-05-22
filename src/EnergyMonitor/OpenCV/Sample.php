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

	function __construct(array $data = NULL)
	{
		if ($data) {
			assert(sizeof($data) == 100);
		}
		$this->data = $data;
	}

	function getImagePath() {
		return 'Sample?action=img&data='.urlencode(base64_encode(
//			implode(',', $this->data)
			pack("c*", ...$this->data)
		));
	}

	function render() {
		$data = \Request::getInstance()->getBase64('data');
//		$this->data = trimExplode(',', $data);
		$this->data = unpack('C*', $data);
//		debug($_REQUEST['data'], strlen($data), sizeof($this->data));
		assert(sizeof($this->data) == 100);
		$this->imgAction(5);
	}

	function imgAction($t = 1) {
		$img = imagecreate($this->rows * $t,
			$this->cols * $t);
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

}

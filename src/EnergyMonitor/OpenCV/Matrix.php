<?php

namespace EnergyMonitor\OpenCV;

class Matrix
{

	/**
	 * @var int
	 */
	protected $rows;

	/**
	 * @var int
	 */
	protected $cols;

	/**
	 * @var bool
	 */
	protected $dt;

	/**
	 * @var float[]
	 */
	protected $data;

	function __construct(array $source)
	{
		$this->rows = $source['rows'];
		$this->cols = $source['cols'];
		$this->dt = $source['dt'];
		$this->data = $source['data'];
	}

	function size()
	{
		return $this->rows;
	}

	function getRows()
	{
		return $this->rows;
	}

	function getCols()
	{
		return $this->cols;
	}

	function getOne($index)
	{
		if ($index < $this->rows) {
			return array_slice($this->data,
				$index * $this->cols, $this->cols);
		}
		return null;
	}

	function getSample($index)
	{
		$data = $this->getOne($index);
		return new Sample($data);
	}

}

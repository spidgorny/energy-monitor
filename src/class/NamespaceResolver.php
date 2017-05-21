<?php

class NamespaceResolver {

	/**
	 * @var Request
	 */
	protected $request;

	function __construct() {
		$this->request = Request::getInstance();
	}

	function getController() {
		$slug = $this->request->getNameless(1);
		return 'EnergyMonitor\\'.$slug;
	}

}

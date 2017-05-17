<?php

/**
 * Created by PhpStorm.
 * User: DEPIDSVY
 * Date: 17.05.2017
 * Time: 11:10
 */
class Index extends \IndexBase
{

	function __construct()
	{
		$this->csp['default-src'][] = 'fonts.googleapis.com';
		$this->csp['default-src'][] = 'fonts.gstatic.com';
		parent::__construct();
	}

	public function initController() {
		TaylorProfiler::start(__METHOD__);
		if (!$this->controller) {
			$slug = $this->request->getControllerString() ?: EnergyMonitor\Home::class;
			//echo 'Slug: ', $slug, BR;
			if ($slug) {
				$this->loadController($slug);
				$this->bodyClasses[] = get_class($this->controller);
			} else {
				throw new Exception404($slug);
			}
		}
		TaylorProfiler::stop(__METHOD__);
	}

	protected function loadController($class) {
		TaylorProfiler::start(__METHOD__);
		if (class_exists($class)) {
			try {
				$this->controller = new $class();
				//			debug($class, get_class($this->controller));
				if (method_exists($this->controller, 'postInit')) {
					$this->controller->postInit();
				}
			} catch (AccessDeniedException $e) {
				$this->error($e->getMessage());
			}
		} else {
			//debug($_SESSION['autoloadCache']);
			$exception = 'Class '.$class.' not found. Dev hint: try clearing autoload cache?';
			unset($_SESSION['AutoLoad']);
			TaylorProfiler::stop(__METHOD__);
			throw new Exception404($exception);
		}
		TaylorProfiler::stop(__METHOD__);
	}

	function renderProfiler() {
		//$pp = new PageProfiler();
		//$content = $pp->render();
		//return $content;
	}

}

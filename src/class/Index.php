<?php

/**
 * Created by PhpStorm.
 * User: DEPIDSVY
 * Date: 17.05.2017
 * Time: 11:10
 */
class Index extends \IndexBase
{

	/**
	 * @var Menu states
	 */
	public $active;

	function __construct(ConfigInterface  $config)
	{
		$this->csp['default-src'][] = 'fonts.googleapis.com';
		$this->csp['default-src'][] = 'fonts.gstatic.com';
		parent::__construct($config);
	}

	public function initController() {
		TaylorProfiler::start(__METHOD__);
		if (!$this->controller) {
			$resolver = new NamespaceResolver([
				'EnergyMonitor\\',
				'EnergyMonitor\\OpenCV\\',
			]);
			$slug = $resolver->getController(true);
			$slug = $slug ?: EnergyMonitor\Home::class;
//			echo 'Slug: ', $slug, BR;
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

	public function render()
	{
		$this->active = (object)[
			basename(\EnergyMonitor\Home::class) => null,
			basename(\EnergyMonitor\CheckVideo::class) => null,
			basename(\EnergyMonitor\AdjustCamera::class) => null,
			basename(\EnergyMonitor\CollectImages::class) => null,
			basename(\EnergyMonitor\CheckTraining::class) => null,
			basename(\EnergyMonitor\CheckTrainingHollow::class) => null,
		];
		$class = get_class($this->getController());
		$class = basename($class);	// remove NS
		$this->active->$class = 'active';
		return parent::render();
	}

	function renderProfiler() {
		//$pp = new PageProfiler();
		//$content = $pp->render();
		//return $content;
	}

}

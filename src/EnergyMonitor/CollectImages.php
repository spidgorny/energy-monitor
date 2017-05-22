<?php

namespace EnergyMonitor;

class CollectImages extends AppController {

	function render() {
		$content = [];
		$files = glob(__DIR__.'/../../cache/*.png');

		$p = new \Pager(75);
		$page = $p->slice($files);
		//debug(sizeof($files), sizeof($page));

		foreach ($page as $file) {
			$content[] = '<img src="cache/'.basename($file).'" width="128" />' . PHP_EOL;
		}

		$content[] = $p->renderPageSelectors($this->getURL());

		return $content;
	}

}

<div style="display: flex">
	<div style="flex: 25%">
		<?php
		$files = glob(__DIR__.'/*.php');
		foreach ($files as $file) {
			echo '<a href="'.basename($file).'">'.
				basename($file).'</a><br />';
		}
		?>
	</div>
	<div>

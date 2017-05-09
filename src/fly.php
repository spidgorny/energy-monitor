<?php

require_once __DIR__.'/../vendor/autoload.php';
require_once __DIR__.'/UploadToGoogleDrive.php';

$uploader = new UploadToGoogleDrive();
$client = $uploader->getClient();
$service = new \Google_Service_Drive($client);

$adapter = new \Hypweb\Flysystem\GoogleDrive\GoogleDriveAdapter($service, '0B36skD0uC-FScXJIbFdLTzZrQlU');

/* Recommended cached adapter use */
// $adapter = new \League\Flysystem\Cached\CachedAdapter(
//     new \Hypweb\Flysystem\GoogleDrive\GoogleDriveAdapter($service, '['root' or folder ID]'),
//     new \League\Flysystem\Cached\Storage\Memory()
// );

$filesystem = new \League\Flysystem\Filesystem($adapter);

//$files = $filesystem->listFiles();
$files = $filesystem->listContents();
print_r($files);

$putOK = $filesystem->put('install.sh', file_get_contents(__DIR__ . '/../install.sh'));
print_r($putOK);

$delOK = $filesystem->delete($files[0]['path']);
print_r($delOK);


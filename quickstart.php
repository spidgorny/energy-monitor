<?php
require_once __DIR__ . '/vendor/autoload.php';

define('APPLICATION_NAME', 'Drive API PHP Quickstart');
define('CREDENTIALS_PATH', '~/.credentials/drive-php-quickstart.json');
define('CLIENT_SECRET_PATH', __DIR__ . '/client_id.json');
// If modifying these scopes, delete your previously saved credentials
// at ~/.credentials/drive-php-quickstart.json

class UploadToGoogleDrive {

	/**
	 * @var Google_Client
	 */
	var $client;

	/**
	 * @var Google_Service_Drive
	 */
	var $service;

	var $scopes = [
		//	Google_Service_Drive::DRIVE_METADATA_READONLY,
		Google_Service_Drive::DRIVE_METADATA,
		Google_Service_Drive::DRIVE_FILE
	];

	public $folderName = 'EnergyMonitor';

	var $folderID;

	function __construct() {
		if (php_sapi_name() != 'cli') {
			throw new Exception('This application must be run on the command line.');
		}
	}

	function render() {
		// Get the API client and construct the service object.
		$this->client = $this->getClient();
		$this->service = new Google_Service_Drive($this->client);

		$this->listFiles();
		$this->folderID = $this->folderExists($this->folderName);
		if (!$this->folderID) {
			$this->folderID = $this->makeFolder();
		}

		$uploadFile = __DIR__ . '/install.sh';
		$fileID = $this->fileExists(basename($uploadFile));
		if (!$fileID) {
			echo 'File exists: ', $fileID, PHP_EOL;
			$this->uploadFile($uploadFile);
		} else {
			echo 'File already exists', PHP_EOL;
			$this->updateFile($fileID, $uploadFile);
		}
	}

	/**
	 * Returns an authorized API client.
	 * @return Google_Client the authorized client object
	 */
	function getClient() {
		$client = new Google_Client();
		$client->setApplicationName(APPLICATION_NAME);
		$client->setScopes($this->scopes);
		$client->setAuthConfig(CLIENT_SECRET_PATH);
		$client->setAccessType('offline');

		// Load previously authorized credentials from a file.
		$credentialsPath = $this->expandHomeDirectory(CREDENTIALS_PATH);
		if (file_exists($credentialsPath)) {
			$accessToken = json_decode(file_get_contents($credentialsPath), true);
		} else {
			// Request authorization from the user.
			$authUrl = $client->createAuthUrl();
			printf("Open the following link in your browser:\n%s\n", $authUrl);
			print 'Enter verification code: ';
			$authCode = trim(fgets(STDIN));

			// Exchange authorization code for an access token.
			$accessToken = $client->fetchAccessTokenWithAuthCode($authCode);

			// Store the credentials to disk.
			if(!file_exists(dirname($credentialsPath))) {
				mkdir(dirname($credentialsPath), 0700, true);
			}
			file_put_contents($credentialsPath, json_encode($accessToken));
			printf("Credentials saved to %s\n", $credentialsPath);
		}
		$client->setAccessToken($accessToken);

		// Refresh the token if it's expired.
		if ($client->isAccessTokenExpired()) {
			$client->fetchAccessTokenWithRefreshToken($client->getRefreshToken());
			file_put_contents($credentialsPath, json_encode($client->getAccessToken()));
		}
		return $client;
	}

	/**
	 * Expands the home directory alias '~' to the full path.
	 * @param string $path the path to expand.
	 * @return string the expanded path.
	 */
	function expandHomeDirectory($path) {
		$homeDirectory = getenv('HOME');
		if (empty($homeDirectory)) {
			$homeDirectory = getenv('HOMEDRIVE') . getenv('HOMEPATH');
		}
		return str_replace('~', realpath($homeDirectory), $path);
	}

	function listFiles() {
		// Print the names and IDs for up to 10 files.
		$optParams = array(
			'pageSize' => 10,
			'fields' => 'nextPageToken, files(id, name)'
		);
		$results = $this->service->files->listFiles($optParams);

		if (count($results->getFiles()) == 0) {
			print "No files found.\n";
		} else {
			print "Files:\n";
			/** @var Google_Service_Drive_DriveFile $file */
			foreach ($results->getFiles() as $file) {
				printf("%s %s (%s)\n", __METHOD__, $file->getName(), $file->getId());
			}
		}
	}

	function folderExists($folderName) {
		$optParams = array(
			'q' => implode(' and ', [
				"name = '{$folderName}'",
				"mimeType = 'application/vnd.google-apps.folder'",
				"trashed = false",
			]),
			'pageSize' => 1,
			'fields' => 'files(id, name)'
		);
		$results = $this->service->files->listFiles($optParams);

		if (count($results->getFiles()) == 0) {
			return NULL;
		} else {
			$folderID = NULL;
			/** @var Google_Service_Drive_DriveFile $file */
			foreach ($results->getFiles() as $file) {
				printf("%s %s (%s)\n", __METHOD__, $file->getName(), $file->getId());
				if ($file->getName() == $this->folderName) {
					$folderID = $file->getId();
				}
			}
			return $folderID;
		}
	}

	function fileExists($fileName) {
		$optParams = array(
			'q' => implode(' and ', [
				"name = '{$fileName}'",
				"mimeType != 'application/vnd.google-apps.folder'",
				"trashed = false",
				"'{$this->folderID}' in parents",
			]),
			'pageSize' => 1,
			'fields' => 'files(id, name)'
		);
		$results = $this->service->files->listFiles($optParams);

		if (count($results->getFiles()) == 0) {
			return NULL;
		} else {
			$fileID = NULL;
			/** @var Google_Service_Drive_DriveFile $file */
			foreach ($results->getFiles() as $file) {
				printf("%s %s (%s)\n", __METHOD__, $file->getName(), $file->getId());
				if ($file->getName() == $fileName) {
					$fileID = $file->getId();
				}
			}
			return $fileID;
		}
	}

	function makeFolder() {
		$fileMetadata = new Google_Service_Drive_DriveFile(array(
			'name' => $this->folderName,
			'mimeType' => 'application/vnd.google-apps.folder'));
		$file = $this->service->files->create($fileMetadata, array(
			'fields' => 'id'));
		printf("Folder ID: %s\n", $file->id);
		return $file->getId();
	}

	function uploadFile($uploadFile) {
		// -- upload
		$fileMetadata = new Google_Service_Drive_DriveFile(array(
			'name' => basename($uploadFile),
			'parents' => array($this->folderID),
		));
		$content = file_get_contents($uploadFile);
		$file = $this->service->files->create($fileMetadata, array(
			'data' => $content,
			'mimeType' => mime_content_type($uploadFile),
			'uploadType' => 'multipart',
			'fields' => 'id'));
		printf("Uploaded File ID: %s\n", $file->id);
	}

	function updateFile($fileID, $uploadFile) {
		try {
			$file = $this->service->files->get($fileID);
			$content = file_get_contents($uploadFile);
			$file = $this->service->files->update($fileID, $file, array(
				'data' => $content,
				'uploadType' => 'multipart',
//				'newRevision' => false,
			));
			printf("Updated File ID: %s\n", $file->id);
		} catch (Exception $e) {
			echo get_class($e), ': ', $e->getMessage(), PHP_EOL;
		}
	}

}

(new UploadToGoogleDrive())->render();

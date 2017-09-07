#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import win32service
import win32file
import win32con
import watchdog
import time
import csvvalid
import csvimport


def directoryWatcher():
	ACTIONS = {
		1 : "Created",
		2 : "Deleted",
		3 : "Updated",
		4 : "Renamed from something",
		5 : "Renamed to something"
	}
	# Thanks to Claudio Grondi for the correct set of numbers
	FILE_LIST_DIRECTORY = 0x0001

	path_to_watch = os.path.dirname(os.path.abspath(__file__))
	parent_dic_cur = str(os.path.join(path_to_watch, os.path.pardir))
	path = "."
	hDir = win32file.CreateFile (
		path_to_watch,
		FILE_LIST_DIRECTORY,
		win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
		None,
		win32con.OPEN_EXISTING,
		win32con.FILE_FLAG_BACKUP_SEMANTICS,
		None
	)
	try:
		logging.basicConfig(filename=parent_dic_cur + "\example.log",level=logging.DEBUG)
		logging.info('Started')
		while 1:
			results = win32file.ReadDirectoryChangesW (
				hDir,
				1024,
				True,
				win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
				win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
				win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
				win32con.FILE_NOTIFY_CHANGE_SIZE |
				win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
				win32con.FILE_NOTIFY_CHANGE_SECURITY,
				None,
				None
			)
				
			for action, file in results:
				full_filename = os.path.join (path, file)
				log = str(full_filename), str(ACTIONS.get (action, "Unknown"))
				logging.info(log)
				if action == 3:
					path_class = csvvalid.CsvValid()
					paths = path_class.pathPicker()
					for path_csv in paths:
						csvimport.ReadCsv(path_csv)
						os.remove(path_csv)
						time.sleep(1)

	except KeyboardInterrupt:
		logging.info('Finished')
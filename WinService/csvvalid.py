#!/usr/bin/python
# -*- coding: utf-8 -*-

from goodtables import validate
import os

class CsvValid:
	def __init__(self):
		self.paths_files = []
		self.path_list = []
		self.path_to_direct = os.path.dirname(os.path.abspath(__file__))
		self.walk = os.walk(".")
		self.paths_files = self.fileMatch()
		self.path_list = self.pathPicker()


	def fileMatch(self):
		for root, dirs, files in self.walk:
			for file in files:
				file = self.path_to_direct + os.sep + file
				self.paths_files.append(file)
		return self.paths_files

	def pathPicker(self):
		for path in self.paths_files:
			report = validate(path)
			if report['tables'][0]['format'] == 'csv':
				colums = report['tables'][0]['headers']
				if len(colums) == 6:
					self.path_list.append(path)
		return self.path_list
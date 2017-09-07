#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys, time
import MySQLdb as mysql
import csv


def ReadCsv(path):
	con = mysql.connect(user="root", passwd="19732525aw")
	cursor = con.cursor()
	sql = 'CREATE DATABASE IF NOT EXISTS WinServCsv;'
	cursor.execute(sql)
	db = mysql.connect("localhost","root","19732525aw","WinServCsv" )
	cursor = db.cursor()
	sql = 'USE WinServCsv;'
	cursor.execute(sql)
	sql = """CREATE TABLE IF NOT EXISTS NOTES (
		Ders  CHAR(20) NOT NULL,
		Ogrenci_no  INT,
		Vize1 INT,  
		Vize2 INT,
		Vize3 INT,
		Final INT)"""
	cursor.execute(sql)

	with open(path) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		data = []
		for row in readCSV:
			if row:
				lesson = row[0]
				student_no = row[1]
				ex1 = row[2]
				ex2 = row[3]
				ex3 = row[4]
				final = row[5]

				data.append([lesson, student_no, ex1, ex2, ex3, final])

		for i in range(1, len(data)-1):
			sql = "INSERT INTO NOTES(Ders,Ogrenci_no, Vize1, Vize2, Vize3, Final) VALUES ('%s', '%d', '%d', '%d', '%d', '%d')" %(str(data[i][0]), int(data[i][1]), int(data[i][2]), int(data[i][3]), int(data[i][4]), int(data[i][5]))
			try:
				cursor.execute(sql)
			except:
				db.rollback()
			db.commit()
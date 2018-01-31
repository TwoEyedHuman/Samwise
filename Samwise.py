import csv
import datetime
import sys

class DayValues:
	Date: datetime
	Open: float
	High: float
	Low: float
	Close: float
	Volume: int
	AdjClose: float

dailyValuesArray = []

dailyValuesFile =  open('V.csv')
dayReader = csv.reader(dailyValuesFile)
for row in dayReader:
	##bufRow = row.split(',')
	bufRow = row
	bufDV = DayValues(
		Date = datetime.datetime.strptime(bufRow[0], '%Y-%m-%d').date(),
		Open = float(bufRow[1]),
		High = float(bufRow[2]),
		Low = float(bufRow[3]),
		Close = float(bufRow[4]),
		Volume = int(bufRow[5]),
		AdjClose = float(bufRow[6])
	)
	dailyValuesArray.append(bufDV)

for day in range(1,5):
	print(dailyValuesArray[day].Date)
	print(dailyValuesArray[day].Open)

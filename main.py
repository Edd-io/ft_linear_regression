from typing import List, Dict
import csv
import sys
import math

PROGRAM_NAME = sys.argv[0]

def parse_data() -> List[Dict[str, int]]:
	"""
	Function to read and parse a CSV file. Returns a list of dictionaries.
	"""

	data = []

	with open('data.csv', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		line = 1

		for row in reader:
			if line == 1:
				if row[0] != "km" and row[1] != "price":
					print(PROGRAM_NAME + ': Invalid file')
			else:
				try:
					data.append({"km": int(row[0]), "price": int(row[1])})
				except:
					print("Line " + str(line) + " invalid : skipped")
			line += 1
	return data

def average_calc(values: List[Dict[str, int]]) -> List[int]:
	"""
	Function to calculate the average.
	"""

	x = 0
	y = 0

	for value in values:
		x += value['km'] 
		y += value['price']
	x /= len(values)
	y /= len(values)
	return [x, y]

def calculate_beta1(averages: List[int], values: List[Dict[str, int]]):
	top = 0
	bot = 0
	for value in values:
		if top == 0:
			top = (value['km'] - averages[0]) * (value['price'] - averages[1])
			bot = math.pow(value['km'] - averages[0], 2)
			continue
		top += (value['km'] - averages[0]) * (value['price'] - averages[1])
		bot += math.pow(value['km'] - averages[0], 2)
	return (top / bot)

def calcultate_beta0(averages: List[int], beta1: int):
	return (averages[1] - (beta1 * averages[0]))

def main():
	data = parse_data()
	avgs = average_calc(data)
	beta1 = calculate_beta1(avgs, data)
	beta0 = calcultate_beta0(avgs, beta1)
	# calcul : beta0 + beta1 * x

if __name__ == '__main__':
	main()

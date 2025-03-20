import matplotlib.pyplot as plt
from typing import List, Dict
import numpy as np
import json
import csv
import sys
import math

PROGRAM_NAME = sys.argv[0]

def parse_data() -> List[Dict[str, float]]:
	"""
	Function to read and parse a CSV file. Returns a list of dictionaries.
	"""

	data = []

	try:
		with open('data.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			line = 1

			for row in reader:
				if line == 1:
					if row[0] != "km" and row[1] != "price":
						print(PROGRAM_NAME + ': Invalid file')
				else:
					try:
						data.append({"km": float(row[0]), "price": float(row[1])})
					except:
						print("Line " + str(line) + " invalid : skipped")
				line += 1
	except:
		print('File "data.csv" not found, incorrect or blocked')
		sys.exit(1)
	return data

def average_calc(values: List[Dict[str, float]]) -> List[float]:
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

def calculate_beta1(averages: List[float], values: List[Dict[str, float]]) -> float:
	"""
	Calculate the slope (beta1) of a simple linear regression model.
	"""

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

def calcultate_beta0(averages: List[float], beta1: float):
	"""
	Calculate the value of beta0 using the averages and beta1.
	"""

	return (averages[1] - (beta1 * averages[0]))

def create_graph(values: List[Dict[str, float]], beta0: float, beta1: float):
	"""
	Show a graph with data
	"""

	for value in values:
		plt.scatter(value['km'], value['price'], color='blue')
	x_min = min(value['km'] for value in values)
	x_max = max(value['km'] for value in values)
	x_line = np.linspace(x_min, x_max, 2)
	y_line = beta0 + beta1 * x_line
	plt.plot(x_line, y_line, '-r', label=f'y = {beta0:.2f} + {beta1:.2f}x')

	plt.xlabel('x - km')
	plt.ylabel('y - price')
	plt.title('ft_linear_regression')
	plt.legend()
	plt.grid()
	plt.show()

def save_in_file(beta0: float, beta1: float):
	"""
	Create a file with data in it
	"""

	data = {
		"beta0": beta0,
		"beta1": beta1
	}
	with open("model.json", "w") as file:
		json.dump(data, file, indent=4)

def evaluate_model(data: List[Dict[str, float]], beta0: float, beta1: float):
	"""
	Calculate and show the precision of model
	"""

	x_values = [value['km'] for value in data]
	y_real = [value['price'] for value in data]
	y_pred = [beta0 + beta1 * x for x in x_values]

	y_mean = sum(y_real) / len(y_real)
	ss_total = sum((yi - y_mean) ** 2 for yi in y_real)
	ss_residual = sum((yi - y_pred_i) ** 2 for yi, y_pred_i in zip(y_real, y_pred))
	r2 = 1 - (ss_residual / ss_total)

	print(f"R²: {r2:.4f} ({(r2 * 100):.0f}% of precision)")

def main():
	if len(sys.argv) > 1:
		print(f'Usage: python {sys.argv[0]}')
		return
	data = parse_data()
	avgs = average_calc(data)
	beta1 = calculate_beta1(avgs, data)
	beta0 = calcultate_beta0(avgs, beta1)
	evaluate_model(data, beta0, beta1)
	save_in_file(beta0, beta1)
	print(f"Beta0: {beta0}, Beta1: {beta1}")
	create_graph(data, beta0, beta1)

if __name__ == '__main__':
	main()

import matplotlib.pyplot as plt
from typing import List, Dict
import numpy as np
import json
import csv
import sys
import math

PROGRAM_NAME = sys.argv[0]
i = 0

def parse_data(file) -> List[Dict[str, float]]:
	data = []
	global i
	try:
		with open(file, newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			line = 1

			for row in reader:
				if line == 1:
					if row[0] != "km" and row[1] != "price":
						raise Exception("Invalid header")
				else:
					try:
						data.append({"km": float(row[0]) + i, "price": float(row[1])})
					except:
						print("Line " + str(line) + " invalid : skipped")
				line += 1
	except:
		print(f'File "{file}" not found, incorrect or blocked. Skipping...')
		return []
	return data

def average_calc(values: List[Dict[str, float]]) -> List[float]:
	x = 0
	y = 0

	for value in values:
		x += value['km'] 
		y += value['price']
	if (len(values) == 0):
		return [0, 0]
	x /= len(values)
	y /= len(values)
	return [x, y]

def create_graph(values: List[Dict[str, float]], theta0: float, theta1: float):
	for value in values:
		plt.scatter(value['km'], value['price'], color='blue')
	x_min = min(value['km'] for value in values)
	x_max = max(value['km'] for value in values)
	x_line = np.linspace(x_min, x_max, 2)
	y_line = theta0 + theta1 * x_line
	plt.plot(x_line, y_line, '-r', label=f'y = {theta0:.2f} + {theta1:.2f}x')

	plt.xlabel('x - km')
	plt.ylabel('y - price')
	plt.title('ft_linear_regression')
	plt.legend()
	plt.grid()
	plt.show()

def save_in_file(theta0: float, theta1: float):
	data = {
		"theta0": theta0,
		"theta1": theta1
	}
	with open("model.json", "w") as file:
		json.dump(data, file, indent=4)

def estimate_price(θ0: float, θ1: float, mileage: float):
	return θ0 + (θ1 * mileage)

def normalize_data(values):
	km = [v['km'] for v in values]
	price = [v['price'] for v in values]
	km_mean = np.mean(km)
	km_std = np.std(km)
	price_mean = np.mean(price)
	price_std = np.std(price)
	return [
		{
			'km': (v['km'] - km_mean) / km_std,
			'price': (v['price'] - price_mean) / price_std
		}
		for v in values
	], (km_mean, km_std, price_mean, price_std)

def training(values: List[Dict[str, float]]):
	values, norms = normalize_data(values)
	km_mean, km_std, price_mean, price_std = norms
	
	tmpθ0 = 0
	tmpθ1 = 0
	learning_rate = 0.1
	for _ in range(1000):
		grad0 = sum(estimate_price(tmpθ0, tmpθ1, v['km']) - v['price'] for v in values)
		grad1 = sum((estimate_price(tmpθ0, tmpθ1, v['km']) - v['price']) * v['km'] for v in values)
		tmpθ0 -= learning_rate * grad0 / len(values)
		tmpθ1 -= learning_rate * grad1 / len(values)
	θ0_real = (tmpθ0 * price_std) - (tmpθ1 * km_mean * price_std)/km_std + price_mean
	θ1_real = tmpθ1 * price_std / km_std
	return θ0_real, θ1_real
		


def evaluate_model(values: List[Dict[str, float]], theta0: float, theta1: float):
	x_values = [value['km'] for value in values]
	y_real = [value['price'] for value in values]
	y_pred = [theta0 + theta1 * x for x in x_values]

	y_mean = sum(y_real) / len(y_real)
	ss_total = sum((yi - y_mean) ** 2 for yi in y_real)
	ss_residual = sum((yi - y_pred_i) ** 2 for yi, y_pred_i in zip(y_real, y_pred))
	r2 = 1 - (ss_residual / ss_total)

	print(f"R²: {r2:.4f} ({(r2 * 100):.0f}% of precision)")

def main():
	data = []

	if len(sys.argv) == 1:
		print(f'Usage: python {sys.argv[0]} <file.csv>')
		return
	for arg in sys.argv[1:]:
		if not arg.endswith('.csv'):
			print(f'File "{arg}" not found, incorrect or blocked. Skipping...')
			continue
		data += parse_data(arg)
	theta0, theta1 = training(data)
	save_in_file(theta0, theta1)
	evaluate_model(data, theta0, theta1)
	create_graph(data, theta0, theta1)

if __name__ == '__main__':
	main()

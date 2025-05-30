import matplotlib.pyplot as plt
import matplotlib
from typing import List, Dict
import numpy as np
import json
import csv
import sys
import argparse

PROGRAM_NAME = sys.argv[0]

args = None

def parse_data(file) -> List[Dict[str, float]]:
	data = []
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
						data.append({"km": float(row[0]), "price": float(row[1])})
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
	try:
		with open("model.json", "w") as file:
			json.dump(data, file, indent=4)
	except:
		print("Error while saving the model in model.json")
		sys.exit(1)

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
	learning_rate = args.l
	for _ in range(args.n):
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

	print(f"R²: {r2:.4f} ({(r2 * 100):.0f}% of precision)", end='\n\n')

def main():
	global args
	data = []

	try:
		parser = argparse.ArgumentParser(description="Train a linear regression model on CSV data.")
		parser.add_argument(
			"files", 
			nargs="+", 
			help="One or more CSV files containing 'km' and 'price' columns."
		)
		parser.add_argument(
			"-l",
			type=float,
			help="Set the learning rate.",
			default=0.1
		)
		parser.add_argument(
			"-n",
			type=int,
			help="Set the number of iterations.",
			default=1000
		)
		parser.add_argument(
			"-g",
			action="store_true",
			help="Display the graph.",
			default=False
		)
		parser.add_argument(
			"-e",
			action="store_true",
			help="Evaluate the model.",
			default=False
		)
		args = parser.parse_args()
	except:
		sys.exit(1)
	if args.l <= 0 or args.l > 1:
		print("Learning rate must be between 0 and 1")
		sys.exit(1)
	if args.n <= 0:
		print("Number of iterations must be greater than 0")
		sys.exit(1)
	for arg in args.files:
		if not arg.endswith('.csv'):
			print(f'File "{arg}" not found, incorrect or blocked. Skipping...')
			continue
		data += parse_data(arg)
	if data == []:
		print("No valid data found. Exiting...")
		sys.exit(0)
	theta0, theta1 = training(data)
	save_in_file(theta0, theta1)
	print("Model saved in model.json")
	if args.e:
		evaluate_model(data, theta0, theta1)
	if args.g:
		create_graph(data, theta0, theta1)

if __name__ == '__main__':
	main()

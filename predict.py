import json
import sys
import matplotlib
import matplotlib.pyplot as plt
import argparse

matplotlib.use('Qt5Agg')
test_mode = False

def get_data():
	try:
		with open('model.json') as jsonfile:
			data = json.load(jsonfile)
	except:
		print(f"\rEstimated selling price: 0€")
		sys.exit(1)
	return data

def plot_linear_model(theta0, theta1, mileage, price):
	plt.figure(figsize=(10, 6))
	x_max = max(300000, mileage * 1.2)
	if theta1 != 0:
		x_intercept = -theta0 / theta1
	else:
		x_intercept = None
	if theta1 == 0:
		plt.hlines(y=max(0, theta0), xmin=0, xmax=x_max, color='r', linewidth=2, label='Linear model')
	elif theta1 < 0 and theta0 > 0 and x_intercept <= x_max:
		plt.plot([0, x_intercept, x_max], [theta0, 0, 0], 'r-', linewidth=2, label='Linear model')
	else:
		y_end = max(0, theta0 + theta1 * x_max)
		plt.plot([0, x_max], [theta0, y_end], 'r-', linewidth=2, label='Linear model')
	plt.hlines(y=price, xmin=0, xmax=mileage, colors='g', linestyles='--', label='Predicted value')
	plt.vlines(x=mileage, ymin=0, ymax=price, colors='b', linestyles='--', label='Vertical projection')
	
	plt.scatter(mileage, price, color='purple', s=100, zorder=3)
	plt.xlim(0, x_max)
	plt.ylim(0, max(price * 1.2, theta0 * 1.2))
	plt.xlabel('Mileage (km)')
	plt.ylabel('Price (€)')
	plt.legend()
	plt.grid(True)
	plt.show()

def main():

	for arg in sys.argv[1:]:
		if arg == '-h' or arg == '--help':
			print(f"Usage: {sys.argv[0]}")
			sys.exit(0)
		elif arg == '-test':
			test_mode = True
			continue
		else:
			print(f"Unknown argument: {arg}")
			sys.exit(1)
	try:
		while True:
			mileage = input('Enter a mileage : ')
			mileage = mileage.strip()
			if len(mileage) == 0:
				print("Can't be null")
				if test_mode:
					sys.exit(0)
				continue
			break
	except:
		if not test_mode:
			print(f"\rEstimated selling price: 0€")
		return
	data = get_data()
	try:
		theta0 = data['theta0']
		theta1 = data['theta1']
	except KeyError:
		print('Invalid model.json file')
		return
	try:
		if (float(mileage) < 0):
			raise Exception()
		price = max(0, theta0 + theta1 * float(mileage))
		print(f"\rEstimated selling price: {price:.2f}€")
		if not test_mode:
			plot_linear_model(theta0, theta1, float(mileage), price)
	except KeyboardInterrupt:
		sys.exit(0)
	except:
		print(f"\rEstimated selling price: 0€")

if __name__ == '__main__':
	main()

import json
import sys
import matplotlib.pyplot as plt

def get_data():
	try:
		with open('model.json') as jsonfile:
			data = json.load(jsonfile)
	except:
		print('File "model.json" not found, incorrect or blocked')
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
	plt.title('Price prediction with zero threshold')
	plt.legend()
	plt.grid(True)
	plt.show()

def main():
	try:
		mileage = float(sys.argv[1])
		if mileage < 0:
			raise ValueError
	except:
		print(f'Usage: python {sys.argv[0]} <mileage (positive number)>')
		return
	data = get_data()
	try:
		theta0 = data['theta0']
		theta1 = data['theta1']
	except KeyError:
		print('Invalid model.json file')
		return
	price = max(0, theta0 + theta1 * mileage)
	print(f"Estimated selling price: {price:.2f}€")
	plot_linear_model(theta0, theta1, mileage, price)

if __name__ == '__main__':
	main()

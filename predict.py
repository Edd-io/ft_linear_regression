import json
import sys

def get_data():
	try:
		with open('model.json') as jsonfile:
			data = json.load(jsonfile)
	except:
		print('File "model.json" not found, incorrect or blocked')
		sys.exit(1)
	return (data)

def main():
	try:
		mileage = float(sys.argv[1])
		if (mileage < 0):
			raise Exception('')
	except:
		print(f'Usage: python {sys.argv[0]} <mileage (positive float)>')
		return
	data = get_data()
	calcul = data['beta0'] + (data['beta1'] * mileage)
	print("Selling price : " + str(max(0, calcul)))

if __name__ == '__main__':
	main()
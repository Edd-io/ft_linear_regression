#!/bin/bash

TEST_NB=1

test()
{
	# arguments:
	# 	$1: with input
	# 	$2: command to run
	#	$3: expected return code
	# 	$4: info

	echo -e "\n\033[1;34m===> Test $TEST_NB\033[0m : \033[1;36m$4\033[0m"
	TEST_NB=$((TEST_NB + 1))
	echo -e "\033[1;38mRunning test: \033[0mpython $2"
	echo -e "\033[1;38mOutput: \033[0m"
	if [ -n "$1" ]; then
		echo "Input: $1"
		output=$(echo $1 | python $2 2>&1)
		ret_code=$?
		echo "$output" | sed 's/^/\t/'
	else
		output=$(python $2 2>&1)
		ret_code=$?
		echo "$output" | sed 's/^/\t/'
	fi
	if [ $ret_code -ne $3 ]; then
		echo "Test failed ❌"
		exit 1
	else
		echo "Test passed ✅"
	fi
	sleep 0.5
}

echo -e "\033[1;34m=======================================\033[0m"
echo -e "\033[1;32m ft_linear_regression tester (initial) \033[0m"
echo -e "\033[1;34m=======================================\033[0m"

echo -e "\033[1;34m===> Cleaning up\033[0m"
rm -rf *.csv
echo "All csv files deleted"
rm -rf *.json
echo -e "All json files deleted\n"
echo -e "\033[1;34m===> Downloading data.csv\033[0m"
wget "https://cdn.intra.42.fr/document/document/30696/data.csv" -O data.csv

echo -e "\033[1;34m=======================================\033[0m"
echo -e "\033[1;32m  ft_linear_regression tester (manda) \033[0m"
echo -e "\033[1;34m=======================================\033[0m"

test "" "train.py" 1 "No input file (train.py)"
test "" "train.py aaa.csv" 0 "Invalid input file (train.py)"
test "" "train.py data.csv" 0 "Valid input file (train.py)"
chmod 000 model.json
test "" "train.py data.csv" 1 "No permission to write model.json (train.py)"
chmod 700 model.json
chmod 000 data.csv
test "" "train.py data.csv" 0 "No permission to read data.csv (train.py)"
chmod 700 data.csv
echo "" > empty.csv
test "" "train.py empty.csv" 0 "Empty input file (train.py)"
echo "corrupted,data" > corrupted.csv
test "" "train.py corrupted.csv" 0 "Corrupted input file (train.py)"
echo "km,price\nabc,def\n123,456" > invalid_data.csv
test "" "train.py invalid_data.csv" 0 "Non-numeric data in input file (train.py)"
echo "km\n1\n2\n3" > missing_column.csv
test "" "train.py missing_column.csv" 0 "Missing column in input file (train.py)"
echo "km,price" > large_data.csv
seq 1 10000 | awk '{print $1","$1*2}' >> large_data.csv
test "" "train.py large_data.csv" 0 "Large input file (train.py)"
test "" "train.py large_data.csv -e" 0 "Large input file with precision (train.py)"
test " " "predict.py -test" 0 "Empty input (predict.py)"
test "" "train.py data.csv" 0 "Valid input file (train.py) (to get valid model.json)"
test "DSADSA" "predict.py -test" 0 "Invalid input (predict.py)"
test "80000" "predict.py -test" 0 "Input = 80000 (predict.py)"
test "150000" "predict.py -test" 0 "Input = 150000 (predict.py)"
test "250000" "predict.py -test" 0 "Input = 250000 (predict.py)"
test "300000" "predict.py -test" 0 "Input = 300000 (predict.py)"
test "500000" "predict.py -test" 0 "Input = 500000 (predict.py)"
test "-80000" "predict.py -test" 0 "Invalid negative input (predict.py)"
test "0" "predict.py -test" 0 "input = 0 (predict.py)"
test "9999999999999999999999999999999999999" "predict.py -test" 0 "input = 9999999999999999999999999999999999999 (predict.py)"
rm model.json
test "50000" "predict.py -test" 1 "Without model.json and value = 50000 (predict.py)"
echo "dsakjdsalkjdsa" > model.json
test "50000" "predict.py -test" 1 "With invalid model.json and value = 50000 (predict.py)"
test "" "predict.py 48928984 29849 89 428942" 1 "With wrong number of arguments (predict.py)"
echo '{"theta0": 0,"theta1": 0}' > model.json
test "50000" "predict.py" 0 "With improbable value in model.json (predict.py)"
echo '{"theta0": -10000,"theta1": -10000}' > model.json
test "50000" "predict.py" 0 "With improbable value in model.json (predict.py)"
echo '{"theta0": 10000000,"theta1": 10000000}' > model.json
test "50000" "predict.py" 0 "With improbable value in model.json (predict.py)"

TEST_NB=1

echo -e "\033[1;34m=======================================\033[0m"
echo -e "\033[1;32m  ft_linear_regression tester (bonus) \033[0m"
echo -e "\033[1;34m=======================================\033[0m"

test "" "train.py data.csv data.csv data.csv data.csv" 0 "Multiple input files (train.py)"
test "" "train.py data.csv -e" 0 "With precision (train.py)"
test "" "train.py data.csv -l 0.01 -e" 0 "Good learning_rate and show precision (train.py)"
test "" "train.py data.csv -l 500" 1 "Bad positive bigger learning_rate(train.py)"
test "" "train.py data.csv -l -1" 1 "Bad negative learning_rate(train.py)"
test "" "train.py data.csv -n 500 -e" 0 "Good number of iterations and show precision (train.py)"
test "" "train.py data.csv -n 0" 1 "Bad number of iterations (train.py)"
test "" "train.py data.csv -n 500 -l 0.01" 0 "Good number of iterations and learning_rate (train.py)"
test "" "train.py data.csv -g" 0 "Show graph (train.py) (close the graph to continue)"
test "" "train.py data.csv -g -e" 0 "Show graph and precision (train.py) (close the graph to continue)"
test "" "train.py data.csv -g -n 500" 0 "Show graph and number of iterations (train.py) (close the graph to continue)"
test "" "train.py data.csv -g -n 500 -e" 0 "Show graph, number of iterations and precision (train.py) (close the graph to continue)"
test "" "train.py data.csv -g -n 10 -l 0.1" 0 "Show graph, number of iterations and learning_rate (train.py) (close the graph to continue)"
test "-10" "predict.py" 0 "Negative input (predict.py)"
test "0" "predict.py" 0 "Zero input (predict.py)"
test "100000" "predict.py" 0 "Positive input with graph (predict.py)"
test "1000000" "predict.py" 0 "Big positive input with graph (predict.py)"
test "100000000000000000000000" "predict.py" 0 "Very big positive input with graph (predict.py)"
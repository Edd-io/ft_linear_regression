#!/bin/bash

TEST_NB=1

test()
{
	# arguments:
	# 	$1: with input
	# 	$2: command to run
	#	$3: expected output
	#	$4: expected return code
	# 	$5: info

	echo -e "\n\033[1;34m===> Test $TEST_NB\033[0m : \033[1;36m$5\033[0m"
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
	if [ $ret_code -ne $4 ]; then
		echo "Test failed ❌"
		echo "Error: $output"
		exit 1
	else
		echo "Test passed ✅"
	fi
	sleep 0.5
}

echo -e "\033[1;34m=======================================\033[0m"
echo -e "\033[1;32m  ft_linear_regression tester (manda) \033[0m"
echo -e "\033[1;34m=======================================\033[0m"

# train.py
test "" "train.py" "" 1 "No input file (train.py)"
test "" "train.py aaa.csv" "" 0 "Invalid input file (train.py)"
test "" "train.py data.csv" "" 0 "Valid input file (train.py)"

# predict.py
test " " "predict.py -test" "" 0 "Empty input (predict.py)"
test "DSADSA" "predict.py -test" "" 0 "Invalid input (predict.py)"
test "80000" "predict.py -test" "" 0 "Input = 80000 (predict.py)"
test "150000" "predict.py -test" "" 0 "Input = 150000 (predict.py)"
test "250000" "predict.py -test" "" 0 "Input = 250000 (predict.py)"
test "300000" "predict.py -test" "" 0 "Input = 300000 (predict.py)"
test "500000" "predict.py -test" "" 0 "Input = 500000 (predict.py)"
test "-80000" "predict.py -test" "" 0 "Invalid negative input (predict.py)"
test "0" "predict.py -test" "" 0 "input = 0 (predict.py)"
test "9999999999999999999999999999999999999" "predict.py -test" "" 0 "input = 9999999999999999999999999999999999999 (predict.py)"
rm model.json
test "50000" "predict.py -test" "" 1 "Without model.json and value = 50000 (predict.py)"
echo "dsakjdsalkjdsa" > model.json
test "50000" "predict.py -test" "" 1 "With invalid model.json and value = 50000 (predict.py)"
rm model.json


TEST_NB=1

echo -e "\033[1;34m=======================================\033[0m"
echo -e "\033[1;32m  ft_linear_regression tester (bonus) \033[0m"
echo -e "\033[1;34m=======================================\033[0m"

test "" "train.py data.csv data.csv data.csv data.csv" "" 0 "Multiple input files (train.py)"
test "" "train.py data.csv -e" "" 0 "With precision (train.py)"
# pas fini

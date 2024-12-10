# Code running instructions
## Instance Generator
### Configuration
To configure the instance generator we need to modify the instance.conf.

This file consists of three parameters n, N and Compatibility Range. 

- n = Array with the number of persons in each department.
- N = Number of participants.
- Compatibility Range = Range between 0 and 1, a random function will set the value on the matrix 
between the first and the second number.

We can configure the n and Compatibility Range so that we can have a more customizable solution.
### Execution
Run the python main. 

It will read the instance.conf file on the specified folder.
### Output 
It will write an output.dat file, in the same folder, with a formatted output as the ones on example project files.

The name of the file can be changed in the end of the main.

## Greedy
### Configuration
The read file can be changed on the python file, the first line of the main.
### Execution
Run the python main.
### Output
It will print in the terminal the committee solution set, the objective function value obtained and the time taken by the calculation.

## Greedy + Local Search
### Configuration
The read file can be changed on the python file, the first line of the main.
### Execution
Run the python main.
### Output
It will print in the terminal the committee solution set, the objective function value obtained and the time taken by the calculation
for the Greedy part and the Local Search part, this can be used in order to test both of them at a time.


## Grasp

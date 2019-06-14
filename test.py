import random


def main():
	test = [range(1,5), range(5,9), range(9,13)]
	print(test)
	holder = []
	switch = []
	for a in range(len(test[0])):
		for b in range(len(test)):
			holder.append(test[b][a])
		switch.append(holder)	
		holder=[]
	
	print(switch)

		

if __name__ == '__main__':
	main()

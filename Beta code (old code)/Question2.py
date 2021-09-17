filenames = os.listdir(pathData)
df = pd.DataFrame()
df['filenames'] = filenames
df1 = df['filenames'].str.split('_', expand=True)
student = pd.DataFrame()
student['Student ID'] = df1[0]
df2 = pd.DataFrame()
df2 = df1[2].str.split('.', expand=True)
studentNames = df1[1].values.tolist()
lastNames = []
surNames = []
firstNames = []
for name in studentNames:
	turn = 0
	count = 0
	tmpLastName = ''
	tmpSurName = ''
	tmpFirstName = ''
	while count <= len(name)-1:
		if name[count].isupper():
			turn += 1
		if turn == 1:
			tmpLastName += name[count]
		if turn == 2:
			tmpSurName += name[count]
		if turn == 3:
			tmpFirstName += name[count]
		count += 1
	lastNames.append(tmpLastName)
	surNames.append(tmpSurName)
	firstNames.append(tmpFirstName)
student['First Name'] = firstNames
student['Sur Name'] = surNames
student['Last Name'] = lastNames
student['Code'] = df2[0]

import os, sys, subprocess

avg = [0, 0, 0]
total = 0
top3 = 0

for i in range(10):
  os.system("python launcher.pyz g")
  out = subprocess.Popen(['python', 'launcher.pyz', 'r'],
  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout,stderr = out.communicate()
  list = stdout.split()
  num = list[len(list)-9]
  temp = str(num).split("'")
  num = int(temp[1])
  total+=num
  if(num > min(avg)):
    avg[avg.index(min(avg))] = num
  print(num)
  # print(stdout)
print("Total average: " + str(total/10))
for i in range(3):
  top3+=avg[i-1]
print("Top 3 average: " + str(top3/3))

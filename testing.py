import os, sys, subprocess

avg = [0, 0, 0]
total = 0

for i in range(30):
  os.system("python launcher.pyz g")
  out = subprocess.Popen(['python', 'launcher.pyz', 'r'],
  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout,stderr = out.communicate()
  list = stdout.split()
  num = list[len(list)-9]
  temp = str(num).split("'")
  num = int(temp[1])
  if(num > min(avg)):
    avg[avg.index(min(avg))] = num
  print(num)
  # print(stdout)
for i in range(3):
  total+=avg[i-1]
print(total/3)

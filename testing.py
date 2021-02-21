import os, sys, subprocess

avg = [0, 0, 0]
total = 0
top3 = 0
deathMessage = ""

for i in range(10):
  os.system("python launcher.pyz g")
  out = subprocess.Popen(['python', 'launcher.pyz', 'r'],
  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout,stderr = out.communicate()
  list = stdout.split()
  death = list[len(list)-16:len(list)-12]
  for word in death:
    deathMessage+=" "
    temp = str(word).split("'")
    word = temp[1]
    deathMessage+=word
  print(deathMessage)
  num = list[len(list)-9]
  turn = list[len(list)-5]
  turn = str(turn).split("'")
  turn = turn[1]
  temp = str(num).split("'")
  num = int(temp[1])
  total+=num
  if(num > min(avg)):
    avg[avg.index(min(avg))] = num
  print("" + str(num) + " renown")
  print("" + str(turn) + " turns")
  deathMessage = ""
  # print(stdout)
print("Total average: " + str(total/10))
for i in range(3):
  top3+=avg[i-1]
print("Top 3 average: " + str(top3/3))

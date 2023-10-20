#i=0
#x=2
#y=3
#while i<10:
    #for z in [x,y]:
       # i += z
    #if x<3:
    #    x+=1

#print(i)



#embedded_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#print(embedded_list[2][2])

#l= []

#while len(l) >=0:
  #  l.append(len(l))
  #  print(l)

l = [0, 1, 1, 2, 3, 5, 8]
a = (sum(l)/ len(l))< len(l)

while a == True:
    l.append(l[-1]+l[-2])
    a= (sum(l)/ len(l))< len(l)
    print(l)
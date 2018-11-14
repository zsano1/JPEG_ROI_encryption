
import numpy as np
filehandle = open('/home/zsa/PycharmProjects/tensorflow-yolo-python2.7/kuang.txt', 'r')
content = np.zeros(4)

for i in range(4):
    content[i]= round(float(filehandle.readline().strip()))
print(content[1]-content[0])



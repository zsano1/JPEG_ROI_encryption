# JPEG_ROI_encryption
two methods including JPEG bitstream method(reversible) and pixel method to detect region of interests and encrypt.

bitstream ROI encryption folder includes the bitstream method of ROI transforming. It is the only method that can both encrypt the ROI and revert to the original bitstream. It can be used in the high_accuracy_requirment condition such as military affairs. Main procedure includes 3 steps.
1.huffman decode in JPEG stream using JPEG standard
2.robust real_time face detection
3.JPEG image encryption with improved format compatibility and file size preservation(upload later)
requirment:
cv2,numpy
run:
cd /home/zsa/JPEG ROI encryption/bitstream ROI encryption/JPEG bitstream huffman_decode
g++ -c tinyjpeg.cxx -o tiny.o
g++ -c huff.cxx -o huff.o
g++ huff.o tiny.o -o hao
./hao
python encode.py
(to be continued)

pixel ROI encryption folder includes the pixel method of ROI transforming. Main procedure includes 3 steps.
1.transform the BMP picture to JPEG 
2.use YOLO_v1 simultaneously to detect region of interests(ROI)
3.use AES encryption method to encrypt the ROI while other regions matain invariant.
requirment:
tensorflow,cv2,numpy,scipy,PIL
run:
cd /home/JPEG ROI encryption/pixel ROI encryption/yolo_v1_BMP
python demo.py 
cd ../JPEG+AES
python demo.py

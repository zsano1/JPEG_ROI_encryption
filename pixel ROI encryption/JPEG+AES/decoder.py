import argparse
import math
import numpy as np
from utils import *
from scipy import fftpack
from PIL import Image
import aes as AES
import numpy as np

class JPEGFileReader:
    TABLE_SIZE_BITS = 16
    BLOCKS_COUNT_BITS = 32

    DC_CODE_LENGTH_BITS = 4
    CATEGORY_BITS = 4

    AC_CODE_LENGTH_BITS = 8
    RUN_LENGTH_BITS = 4
    SIZE_BITS = 4

    def __init__(self, filepath):
        self.__file = open(filepath, 'r')

    def read_int(self, size):
        if size == 0:
            return 0

        # the most significant bit indicates the sign of the number
        bin_num = self.__read_str(size)
        if bin_num[0] == '1':
            return self.__int2(bin_num)
        else:
            return self.__int2(binstr_flip(bin_num)) * -1

    def read_dc_table(self):
        table = dict()

        table_size = self.__read_uint(self.TABLE_SIZE_BITS)
        for _ in range(table_size):
            category = self.__read_uint(self.CATEGORY_BITS)
            code_length = self.__read_uint(self.DC_CODE_LENGTH_BITS)
            code = self.__read_str(code_length)
            table[code] = category
        return table

    def read_ac_table(self):
        table = dict()

        table_size = self.__read_uint(self.TABLE_SIZE_BITS)
        for _ in range(table_size):
            run_length = self.__read_uint(self.RUN_LENGTH_BITS)
            size = self.__read_uint(self.SIZE_BITS)
            code_length = self.__read_uint(self.AC_CODE_LENGTH_BITS)
            code = self.__read_str(code_length)
            table[code] = (run_length, size)
        return table

    def read_blocks_count(self):
        return self.__read_uint(self.BLOCKS_COUNT_BITS)

    def read_huffman_code(self, table):
        prefix = ''
        # TODO: break the loop if __read_char is not returing new char
        while prefix not in table:
            prefix += self.__read_char()
        return table[prefix]

    def __read_uint(self, size):
        if size <= 0:
            raise ValueError("size of unsigned int should be greater than 0")
        return self.__int2(self.__read_str(size))

    def __read_str(self, length):
        return self.__file.read(length)

    def __read_char(self):
        return self.__read_str(1)

    def __int2(self, bin_num):
        return int(bin_num, 2)


def read_image_file(filepath):
    reader = JPEGFileReader(filepath)

    tables = dict()
    for table_name in ['dc_y', 'ac_y', 'dc_c', 'ac_c']:
        if 'dc' in table_name:
            tables[table_name] = reader.read_dc_table()
        else:
            tables[table_name] = reader.read_ac_table()

    blocks_count = reader.read_blocks_count()

    dc = np.empty((blocks_count, 3), dtype=np.int32)
    ac = np.empty((blocks_count, 63, 3), dtype=np.int32)

    for block_index in range(blocks_count):
        for component in range(3):
            dc_table = tables['dc_y'] if component == 0 else tables['dc_c']
            ac_table = tables['ac_y'] if component == 0 else tables['ac_c']

            category = reader.read_huffman_code(dc_table)
            dc[block_index, component] = reader.read_int(category)

            cells_count = 0

            # TODO: try to make reading AC coefficients better
            while cells_count < 63:
                run_length, size = reader.read_huffman_code(ac_table)

                if (run_length, size) == (0, 0):
                    while cells_count < 63:
                        ac[block_index, cells_count, component] = 0
                        cells_count += 1
                else:
                    for i in range(run_length):
                        ac[block_index, cells_count, component] = 0
                        cells_count += 1
                    if size == 0:
                        ac[block_index, cells_count, component] = 0
                    else:
                        value = reader.read_int(size)
                        ac[block_index, cells_count, component] = value
                    cells_count += 1

    return dc, ac, tables, blocks_count


def zigzag_to_block(zigzag):
    # assuming that the width and the height of the block are equal
    rows = cols = int(math.sqrt(len(zigzag)))

    if rows * cols != len(zigzag):
        raise ValueError("length of zigzag should be a perfect square")

    block = np.empty((rows, cols), np.int32)

    for i, point in enumerate(zigzag_points(rows, cols)):
        block[point] = zigzag[i]

    return block


def dequantize(block, component):
    q = load_quantization_table(component)
    return block * q


def idct_2d(image):
    return fftpack.idct(fftpack.idct(image.T, norm='ortho').T, norm='ortho')


def main():


    dc, ac, tables, blocks_count = read_image_file('/home/zsa/ttt')

    # assuming that the block is a 8x8 square
    block_side = 8

    # assuming that the image height and width are equal
    image_side = int(math.sqrt(blocks_count)) * block_side

    blocks_per_line = image_side // block_side

    npmat = np.empty((image_side, image_side, 3), dtype=np.uint8)

    for block_index in range(blocks_count):
        i = block_index // blocks_per_line * block_side
        j = block_index % blocks_per_line * block_side

        for c in range(3):
            zigzag = [dc[block_index, c]] + list(ac[block_index, :, c])
            quant_matrix = zigzag_to_block(zigzag)
            dct_matrix = dequantize(quant_matrix, 'lum' if c == 0 else 'chrom')
            block = idct_2d(dct_matrix)
            npmat[i:i+8, j:j+8, c] = block + 128

    n=np.zeros(image_side*image_side*3)
    m=np.zeros(64)
    mn=np.empty((image_side,image_side,3),dtype=np.uint8)
    pp = np.zeros(image_side * image_side * 3)



    index=0
    for i in range(image_side):
        for j in range(image_side):
            for k in range(3):
                n[index] = npmat[i][j][k]
                index+=1
    index=0
    o=0
    shu=0
    ind=0
    w=0
    a=0
    q=0
    oo=0
    uu=0
    u = 15
    p = np.zeros(16)
    print('xxx',n[16:32])
    for j in range(image_side*image_side*3/16):
        for i in range(16):
            m[ind]=n[index]
            s=long(m[ind])
            shu+=s
            shu=long(shu*256)
            index += 1
            ind+=1
        ind=0
        shu=long(shu/256)
        h=AES.obj.encrypt(shu)
        shu=0
        for x in range(16):
            p[u]=h%256
            h=h/256
            u=u-1
        for jj in range(16):
            pp[o]=p[oo]
            o+=1
            oo+=1
        oo=0
        u=15
    for i in range(image_side):
        for j in range(image_side):
            for k in range(3):
                mn[a,w,q]=pp[uu]
                q+=1
                uu+=1
            q=0
            w+=1
        w=0
        a+=1
    print('zsa',pp[16:32])

    n=np.zeros(image_side*image_side*3)
    m=np.zeros(64)
    nn=np.empty((image_side,image_side,3),dtype=np.uint8)
    pp = np.zeros(image_side * image_side * 3)
    index=0
    for i in range(image_side):
        for j in range(image_side):
            for k in range(3):
                n[index] = mn[i][j][k]
                index+=1
    index=0
    o=0
    shu=0
    ind=0
    w=0
    a=0
    q=0
    oo=0
    uu=0
    u = 15
    p = np.zeros(16)
    for j in range(image_side*image_side*3/16):
        for i in range(16):
            m[ind]=n[index]
            s=long(m[ind])
            shu+=s
            shu=long(shu*256)
            index += 1
            ind+=1
        ind=0
        shu=long(shu/256)
        h=AES.obj.decrypt(shu)
        shu = 0
        for x in range(16):
            p[u]=h%256
            h=h/256
            u=u-1

        for jj in range(16):
            pp[o]=p[oo]
            o+=1
            oo+=1
        oo=0
        u=15
    for i in range(image_side):
        for j in range(image_side):
            for k in range(3):
                nn[a,w,q]=pp[uu]
                q+=1
                uu+=1
            q=0
            w+=1
        w=0
        a+=1
    image = Image.fromarray(mn, 'YCbCr')
    image = image.convert('RGB')
    image.show()
    image.save('/home/zsa/man2.jpeg')


if __name__ == "__main__":
    main()

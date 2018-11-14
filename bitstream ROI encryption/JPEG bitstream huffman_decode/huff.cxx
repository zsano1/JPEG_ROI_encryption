
#include "tinyjpeg.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <cstdio>
#include <iostream>
//#define  snprintf _snprintf
//extern char error_string[256];
//static void exitmessage(const char *message) //__attribute__((noreturn));


static int filesize(FILE *fp)
{
  long pos;
  fseek(fp, 0, SEEK_END);
  pos = ftell(fp);
  fseek(fp, 0, SEEK_SET);
  return pos;
}

/**
 * Save a buffer in 24bits Targa format 
 * (BGR byte order)
 */
static void write_tga(const char *filename, int output_format, int width, int height, int **components)
{
  unsigned char targaheader[18];
  FILE *F;
  char temp[1024];
  unsigned int bufferlen = width * height * 3;
  int *rgb_data = components[0];

  snprintf(temp, sizeof(temp), filename);

  memset(targaheader,0,sizeof(targaheader));

  targaheader[12] = (unsigned char) (width & 0xFF);
  targaheader[13] = (unsigned char) (width >> 8);
  targaheader[14] = (unsigned char) (height & 0xFF);
  targaheader[15] = (unsigned char) (height >> 8);
  targaheader[17] = 0x20;    /* Top-down, non-interlaced */
  targaheader[2]  = 2;       /* image type = uncompressed RGB */
  targaheader[16] = 24;

  if (output_format == TINYJPEG_FMT_RGB24)
   {
     int *data = rgb_data + bufferlen - 3;
     do
      { 
	int c = data[0];
	data[0] = data[2];
	data[2] = c;
	data-=3;
      }
     while (data > rgb_data);
   }

  F = fopen(temp, "wb");
  fwrite(targaheader, sizeof(targaheader), 1, F);
  fwrite(rgb_data, 1, bufferlen, F);
  fclose(F);
}

/**
 * Save a buffer in three files (.Y, .U, .V) useable by yuvsplittoppm
 */
static void write_yuv(const char *filename, int width, int height, int **components)
{
  FILE *F;
  char temp[1024];

#ifdef TRACE
  FILE *yuv_file;
  snprintf(temp, 1024, "%s.YUV", filename);
  yuv_file = fopen(temp,"wb");
  fwrite(components[0], width, height, yuv_file);
  fwrite(components[1], width*height/4,1, yuv_file);
  fwrite(components[2], width*height/4,1, yuv_file);
#endif

  snprintf(temp, 1024, "%s.Y", filename);
  F = fopen(temp, "wb");
  fwrite(components[0], width, height, F);
  fclose(F);
  snprintf(temp, 1024, "%s.U", filename);
  F = fopen(temp, "wb");
  fwrite(components[1], width*height/4, 1, F);
  fclose(F);
  snprintf(temp, 1024, "%s.V", filename);
  F = fopen(temp, "wb");
  fwrite(components[2], width*height/4, 1, F);
  fclose(F);
}

/**
 * Save a buffer in grey image (pgm format)
 */
static void write_pgm(const char *filename, int width, int height, int **components)
{
  FILE *F;
  char temp[1024];

  snprintf(temp, 1024, "%s", filename);
  F = fopen(temp, "wb");
  fprintf(F, "P5\n%d %d\n255\n", width, height);
  fwrite(components[0], width, height, F);
  fclose(F);
}



/**
 * Load one jpeg image, and decompress it, and save the result.
 */
int convert_one_image(const char *infilename, const char *outfilename, int output_format)
{
  FILE *fp;
  unsigned int length_of_file;
  unsigned int width, height;
  unsigned char *buf;
  struct jdec_private *jdec;
  int *components[3];

  /* Load the Jpeg into memory */
  fp = fopen(infilename, "rb");

  length_of_file = filesize(fp);
  buf = (unsigned char *)malloc(length_of_file + 4);

  fread(buf, length_of_file, 1, fp);
  fclose(fp);

  /* Decompress it */
  jdec = tinyjpeg_init();
 

  tinyjpeg_parse_header(jdec, buf, length_of_file);
  std::cout<<"asdasd";
  /* Get the size of the image */
  tinyjpeg_get_size(jdec, &width, &height);


  tinyjpeg_decode(jdec, output_format);

  /* 
   * Get address for each plane (not only max 3 planes is supported), and
   * depending of the output mode, only some components will be filled 
   * RGB: 1 plane, YUV420P: 3 planes, GREY: 1 plane
   */

  /* Only called this if the buffers were allocated by tinyjpeg_decode() */
  tinyjpeg_free(jdec);
  /* else called just free(jdec); */

  free(buf);
  return 0;
}

static void usage(void)
{
    fprintf(stderr, "Usage: loadjpeg [options] <input_filename.jpeg> <format> <output_filename>\n");
    fprintf(stderr, "options:\n");
    fprintf(stderr, "  --benchmark - Convert 1000 times the same image\n");
    fprintf(stderr, "format:\n");
    fprintf(stderr, "  yuv420p - output 3 files .Y,.U,.V\n");
    fprintf(stderr, "  rgb24   - output a .tga image\n");
    fprintf(stderr, "  bgr24   - output a .tga image\n");
    fprintf(stderr, "  gray    - output a .pgm image\n");
    exit(1);
}

/**
 * main
 *
 */
FILE *p_trace;
bool show_db=false;
int main()
{

  int output_format = TINYJPEG_FMT_YUV420P;
  char *output_filename, *input_filename;
  clock_t start_time, finish_time;
  output_filename="/home/zsa/info.txt";
  input_filename="test.jpg";
  std::cout<<"a";
  convert_one_image(input_filename, output_filename, output_format);
    
  std::cout<<"asdasd";

}





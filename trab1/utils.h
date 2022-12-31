#ifndef __UTILS_H__
#define __UTILS_H__

#include <stdio.h>
#include <stdlib.h>

void readArrayFromKeyboard(double *array, uint size);
void readMatrixFromKeyboard(double **matrix, uint lineQnt, uint colsQnt);
void initCrescentMatrix(uint **matrix, uint lineQnt, uint colsQnt, uint startingInt);
void printUintArray(uint *array, uint size);
void printDoubleArray(double *array, uint size);
void printUintMatrix(uint **matrix, uint lineQnt, uint colsQnt);
void printDoubleMatrix(double **matrix, uint lineQnt, uint colsQnt);

#endif
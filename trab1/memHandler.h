#ifndef __MEM_HANDLER_H__
#define __MEM_HANDLER_H__

#include <stdio.h>
#include <stdlib.h>

void freeDoubleArray(double *array);
void freeDoubleMatrix(double **matrix, uint linesQnt);
void freeUintMatrix(uint **matrix, uint linesQnt);
double *allocDoubleArray(uint size);
double **allocDoubleMatrix(uint linesQnt, uint colsQnt);
uint **allocUintMatrix(uint linesQnt, uint colsQnt);

#endif
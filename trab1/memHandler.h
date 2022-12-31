#ifndef __MEM_HANDLER_H__
#define __MEM_HANDLER_H__

#include <stdio.h>
#include <stdlib.h>

#include "memHandler.h"

void freeDoubleArray(double *array);
void freeDoubleMatrix(double **matrix, uint linesQnt);
void freeUintArray(uint *array);
void freeUintMatrix(uint **matrix, uint linesQnt);
double *allocDoubleArray(uint size);
uint *allocUintArray(uint size);
double **allocDoubleMatrix(uint linesQnt, uint colsQnt);
uint **allocUintMatrix(uint linesQnt, uint colsQnt);

#endif
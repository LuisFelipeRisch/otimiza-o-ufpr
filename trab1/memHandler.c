#include "memHandler.h"

void freeDoubleArray(double *array){
  if(!array)
    return;

  free(array);
}

void freeDoubleMatrix(double **matrix, uint linesQnt){
  if(!matrix)
    return;

  for(uint i = 0; i < linesQnt; i++)
    freeDoubleArray(matrix[i]);

  free(matrix);
}

void freeUintArray(uint *array){
  if(!array)
    return;

  free(array);
}

void freeUintMatrix(uint **matrix, uint linesQnt){
  if(!matrix)
    return;

  for(uint i = 0; i < linesQnt; i++)
    freeUintArray(matrix[i]);

  free(matrix);
}

double *allocDoubleArray(uint size){
  double *array = calloc(size, sizeof(double));

  if(!array)
    return NULL;

  return array;
}

uint *allocUintArray(uint size){
  uint *array = calloc(size, sizeof(uint));

  if(!array)
    return NULL;

  return array;
}

double **allocDoubleMatrix(uint linesQnt, uint colsQnt){
  double **matrix = calloc(linesQnt, sizeof(double *));

  if (!matrix)
    return NULL;

  for (uint i = 0; i < linesQnt; i++){
    matrix[i] = allocDoubleArray(colsQnt);

    if (!matrix[i]){
      for (uint j = i - 1; j >= 0; j--)
        freeDoubleArray(matrix[j]);
      free(matrix);

      return NULL;
    }
  }

  return matrix;
}

uint **allocUintMatrix(uint linesQnt, uint colsQnt){
  uint **matrix = calloc(linesQnt, sizeof(uint *));

  if (!matrix)
    return NULL;

  for (uint i = 0; i < linesQnt; i++){
    matrix[i] = allocUintArray(colsQnt);

    if (!matrix[i]){
      for (uint j = i - 1; j >= 0; j--)
        freeUintArray(matrix[j]);
      free(matrix);

      return NULL;
    }
  }

  return matrix;
}


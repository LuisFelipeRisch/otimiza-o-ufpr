#include "utils.h"

void readMatrixFromKeyboard(double **matrix, uint lineQnt, uint colsQnt){
  for (uint i = 0; i < lineQnt; i++)
    for(uint j = 0; j < colsQnt; j++)
      scanf("%lg", &(matrix[i][j]));
}

void readArrayFromKeyboard(double *array, uint size){
  for (uint i = 0; i < size; i++)
    scanf("%lg", &array[i]);
}

void initCrescentMatrix(uint **matrix, uint lineQnt, uint colsQnt, uint startingInt){
  for (uint i = 0; i < lineQnt; i++)
    for(uint j = 0; j < colsQnt; j++)
    {
      matrix[i][j] = startingInt;
      startingInt += 1;
    }
}
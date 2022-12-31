#ifndef __PROBLEM_H__
#define __PROBLEM_H__

#include <stdio.h>
#include <stdlib.h>
#include "memHandler.h"
#include "utils.h"

typedef struct
{
  uint   factoriesQnt;
  uint   citiesQnt;
  double *factoriesCapacities;
  double *citiesDemands;
  double **transportCost;
  uint   **problemVars;
} PROBLEM_STRUCT;

PROBLEM_STRUCT *initProblem();
void printProblem(PROBLEM_STRUCT *problem);
void printProblemAsLP(PROBLEM_STRUCT *problem);
void freeProblemStruct(PROBLEM_STRUCT *problem);


#endif
#include "problem.h"

void freeProblemStruct(PROBLEM_STRUCT *problem){
  if(!problem)
    return;

  freeDoubleMatrix(problem->transportCost, problem->factoriesQnt);
  freeUintMatrix(problem->problemVars, problem->factoriesQnt);
  freeDoubleArray(problem->factoriesCapacities);
  freeDoubleArray(problem->citiesDemands);
  free(problem);
}

PROBLEM_STRUCT *initProblem(){
  PROBLEM_STRUCT *problem = malloc(sizeof(PROBLEM_STRUCT));
  if(!problem)
    return NULL;

  scanf("%d", &problem->factoriesQnt);
  scanf("%d", &problem->citiesQnt);

  problem->factoriesCapacities = allocDoubleArray(problem->factoriesQnt);
  if(!problem->factoriesCapacities)
  {
    freeProblemStruct(problem);
    return NULL;
  }
  readArrayFromKeyboard(problem->factoriesCapacities, problem->factoriesQnt);

  problem->citiesDemands = allocDoubleArray(problem->citiesQnt);
  if(!problem->citiesDemands){
    freeProblemStruct(problem);
    return NULL;
  }
  readArrayFromKeyboard(problem->citiesDemands, problem->citiesQnt);

  problem->transportCost = allocDoubleMatrix(problem->factoriesQnt, problem->citiesQnt);
  if (!problem->transportCost){
    freeProblemStruct(problem);
    return NULL;
  }
  readMatrixFromKeyboard(problem->transportCost, problem->factoriesQnt, problem->citiesQnt);

  problem->problemVars = allocUintMatrix(problem->factoriesQnt, problem->citiesQnt);
  if (!problem->problemVars){
    freeProblemStruct(problem);
    return NULL;
  }
  initCrescentMatrix(problem->problemVars, problem->factoriesQnt, problem->citiesQnt, 1);

  return problem;
}

void printObjectiveFunction(PROBLEM_STRUCT *problem){
  uint i, j;

  printf("min: ");
  for (i = 0; i < problem->factoriesQnt; i++)
    for (j = 0; j < problem->citiesQnt; j++)
    {
      printf("%.15gx%d", problem->transportCost[i][j], problem->problemVars[i][j]);

      if(i != problem->factoriesQnt - 1 || j != problem->citiesQnt - 1)
        printf(" + ");
    }
  printf(";");
}

void printConstrains(PROBLEM_STRUCT *problem){
  uint i, j;

  for(i = 0; i < problem->factoriesQnt; i++){
    for (j = 0; j < problem->citiesQnt; j++){
      printf("x%d", problem->problemVars[i][j]);

      if(j != problem->citiesQnt - 1)
        printf(" + ");
    }
    printf(" <= %.15g;\n", problem->factoriesCapacities[i]);
  }
  for(i = 0; i < problem->citiesQnt; i++){
    for (j = 0; j < problem->factoriesQnt; j++){
      printf("x%d", problem->problemVars[j][i]);

      if(j != problem->factoriesQnt - 1)
        printf(" + ");
    }
    printf(" >= %.15g;\n", problem->citiesDemands[i]);
  }
  for (i = 0; i < problem->factoriesQnt; i++)
    for (j = 0; j < problem->citiesQnt; j++)
      printf("x%d >= 0;\n", problem->problemVars[i][j]);
}

void printProblemAsLP(PROBLEM_STRUCT *problem){
  printObjectiveFunction(problem);
  printf("\n");
  printConstrains(problem);
}
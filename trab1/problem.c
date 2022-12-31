#include "problem.h"

PROBLEM_STRUCT *initProblem(){
  PROBLEM_STRUCT *problem = malloc(sizeof(PROBLEM_STRUCT));
  if(!problem)
    return NULL;

  scanf("%d", &problem->factoriesQnt);
  scanf("%d", &problem->citiesQnt);

  problem->factoriesCapacities = allocDoubleArray(problem->factoriesQnt);
  if(!problem->factoriesCapacities)
    return NULL;
  readArrayFromKeyboard(problem->factoriesCapacities, problem->factoriesQnt);

  problem->citiesDemands = allocDoubleArray(problem->citiesQnt);
  if(!problem->citiesDemands)
    return NULL;
  readArrayFromKeyboard(problem->citiesDemands, problem->citiesQnt);

  problem->transportCost = allocDoubleMatrix(problem->factoriesQnt, problem->citiesQnt);
  if (!problem->transportCost)
    return NULL;
  readMatrixFromKeyboard(problem->transportCost, problem->factoriesQnt, problem->citiesQnt);

  problem->problemVars = allocUintMatrix(problem->factoriesQnt, problem->citiesQnt);
  if (!problem->problemVars)
    return NULL;
  initCrescentMatrix(problem->problemVars, problem->factoriesQnt, problem->citiesQnt, 1);

  return problem;
}

void printProblem(PROBLEM_STRUCT *problem){
  printf("%d %d", problem->factoriesQnt, problem->citiesQnt);
  printf("\n");
  printDoubleArray(problem->factoriesCapacities, problem->factoriesQnt);
  printf("\n");
  printDoubleArray(problem->citiesDemands, problem->citiesQnt);
  printf("\n");
  printDoubleMatrix(problem->transportCost, problem->factoriesQnt, problem->citiesQnt);
  printf("\n");
  printUintMatrix(problem->problemVars, problem->factoriesQnt, problem->citiesQnt);
}

void printObjectiveFunction(PROBLEM_STRUCT *problem){
  printf("min: ");
  for (uint i = 0; i < problem->factoriesQnt; i++)
    for (uint j = 0; j < problem->citiesQnt; j++)
    {
      printf("%.15gx%d", problem->transportCost[i][j], problem->problemVars[i][j]);

      if(i != problem->factoriesQnt - 1 || j != problem->citiesQnt - 1)
        printf(" + ");
    }
  printf(";");
}

void printConstrains(PROBLEM_STRUCT *problem){
  for(uint i = 0; i < problem->factoriesQnt; i++){
    for (uint j = 0; j < problem->citiesQnt; j++){
      printf("x%d", problem->problemVars[i][j]);

      if(j != problem->citiesQnt - 1)
        printf(" + ");
    }
    printf(" <= %.15g;\n", problem->factoriesCapacities[i]);
  }
  for(uint i = 0; i < problem->citiesQnt; i++){
    for (uint j = 0; j < problem->factoriesQnt; j++){
      printf("x%d", problem->problemVars[j][i]);

      if(j != problem->factoriesQnt - 1)
        printf(" + ");
    }
    printf(" >= %.15g;\n", problem->citiesDemands[i]);
  }
  for (uint i = 0; i < problem->factoriesQnt; i++)
    for (uint j = 0; j < problem->citiesQnt; j++)
      printf("x%d >= 0;\n", problem->problemVars[i][j]);
}

void printProblemAsLP(PROBLEM_STRUCT *problem){
  printObjectiveFunction(problem);
  printf("\n");
  printConstrains(problem);
}

void freeProblemStruct(PROBLEM_STRUCT *problem){
  freeDoubleMatrix(problem->transportCost, problem->factoriesQnt);
  freeUintMatrix(problem->problemVars, problem->factoriesQnt);
  freeDoubleArray(problem->factoriesCapacities);
  freeDoubleArray(problem->citiesDemands);
  free(problem);
}
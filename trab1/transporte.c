#include <stdio.h>
#include <stdlib.h>
#include "problem.h"

int main(){
  PROBLEM_STRUCT *problem = initProblem();
  if(problem)
    printProblemAsLP(problem);

  freeProblemStruct(problem);

  return 0;
}
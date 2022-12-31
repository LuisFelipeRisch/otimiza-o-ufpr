#include <stdio.h>
#include <stdlib.h>
#include "problem.h"

int main(){
  PROBLEM_STRUCT *problem = initProblem();

  printProblem(problem);
  printf("\n\n-- LP --\n\n");
  printProblemAsLP(problem);

  freeProblemStruct(problem);
  return 0;
}
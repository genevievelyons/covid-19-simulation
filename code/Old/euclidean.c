#include <stdio.h>
#include<math.h>
//function to find distance bewteen 2 points
float dis(float x1, float y1, float x2, float y2) {
   float distance = sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
   return distance;
}
int main() {
   int l =5;
   float x[5] = {1,2,3,4,5};
   float y[5] ={0,1,2,3,4};
   float r[l][l];

int i, j;

   for(i=0; i<l; i++) {
      for(j=0;j<l;j++) {
         r[i][j] = dis(x[i], y[i], x[j], y[j]);
         printf("r[%d][%d] = %f\n", i,j, r[i][j]);
      }
   }
}
'
'
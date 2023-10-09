#include <stdio.h>

int main()
{
   int a[5];
   int num;
   int i;
   printf("enter element in an array");
   for(int i=0;i<5;i++){
       scanf("%d",&a[i]);
       
       
       
   }
   for(i=0;i<5;i=i+2){
      a[i]=a[i] *2;
       
   }
   printf("modified elements are");
   for(i=0;i<5;i++){
   printf("%d\n",a[i]);
   }
}

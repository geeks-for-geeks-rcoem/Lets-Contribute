// Online C compiler to run C program online
#include <stdio.h>
#define max 10
int main() {
    int n , m[10];
    int a[10] , j=0 ;
    int i =0 ;
    printf("Enter a number of element you want to enter \n");
    scanf("%d",&n);
    printf("Enter the elements\n");
    for(i = 0 ; i<n ; i++)
    {
        scanf("%d",&a[i]);
    }
    
    printf("The Numbers are ");
    for(i = 0 ; i < n ; i++)
    {
        if(a[i] % 2 == 0)
        {
            m[j] = a[i] * 2;
        }
    }
    for(i = 0 ; i < n ; i++)
    {
        printf("\n %d",m[j]);
    }
    return 0;
}
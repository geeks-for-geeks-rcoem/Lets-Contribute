#include <stdio.h>
int main(){
    int n;
    printf("Enter the number you are going to enter in array:\n");
    scanf("%d",&n);
    int arr[n];
    printf("Enter numbers in order\n");
    for (int i = 0; i < n; i++)
    {
        printf("Enter number %d: \n",i+1);
        scanf("%d",&arr[i]);
    }
    printf("The output you asked is:\n");
    for (int i = 0; i < n; i=i+2)
    {
        int temp = arr[i] * 2;
        printf("%d  ", temp);
    }
    return 0;   
}
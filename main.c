#include<stdio.h>
int main(){
    printf("Enter array size");
    int s ;
    scanf("%d",s);
    int a[s]; 
    for(int i =0; i<a; i++){
        scanf("%d",a[i]);
    }
    for(int i =0; i<a; i++){
        if(a[i]%2==0){
            printf("%d",a[i]);
        }
    }
}
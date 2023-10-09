#include <stdio.h>

int main()
{
    int n;
    printf("Enter the size of the array: ");
    scanf("%d", &n);

    int arr[n];

    printf("Enter the elements of the array: ");
    for (int i = 0; i < n; i++)
    {
        scanf("%d", &arr[i]);
    }

    printf("The elements of the array at even indices * 2  are: ");
    for (int i = 0; i < n; i += 2)
    {
        printf("%d ", arr[i]*2);
    }

    return 0;
}

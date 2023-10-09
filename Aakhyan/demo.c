#include <stdio.h>
#include <stdlib.h>

int main()
{
	int n;
	printf("Enter the size of the array: ");
	scanf("%d", &n);
	int *arr = (int *)malloc(n * sizeof(int));
	printf("Enter the elements of the array: ");
	for (int i = 0; i < n; i++)
	{
		scanf("%d", &arr[i]);
	}
	printf("The elements of the array at even indices are: ");
	for (int i = 0; i < n; i += 2)
	{
		printf("%d ", arr[i]);
	}
	return 0;
}
#include <windows.h>
#include <iostream>
using namespace std;
int main()
{
	int unit=1000;
	Sleep(20*unit);/* VC ??Sleep*/
	cout << "20s done!" << endl;
	return 0;
}

#define MT_REQUEST_TEST_DATA 101
#define MT_TEST_DATA 102

#define MT_GO_L 103
#define MT_GO_R 104

typedef struct 
{ 
    int a; 
    int b; 
    double x; 
} MDF_TEST_DATA;

typedef struct
{
    short pressedL; // boolean [0 or 1]
} MDF_GO_L;

typedef struct
{
    short pressedR; // boolean [0 or 1]
} MDF_GO_R;


#include <vector>
#include <map>
#include <any>

namespace chiakilisp {

typedef std::vector<std::any> vec_t;
typedef std::map<std::any, std::any> map_t;

float add(...);

float sub(...);

float div(...);

float mul(...);

void print(...);

vec_t* vec(...);

map_t* map(...);

}

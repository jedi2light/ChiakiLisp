#include <iostream>
#include <vector>
#include <iterator>
#include <type_traits>

#define nil NULL;

namespace chiakilisp {

template<typename T>
class vector : public std::vector<T> {
public:
    friend std::ostream& operator<<(std::ostream& os, const vector<T>& s) {
        std::cout << "[";

        for (auto iter = s.begin(); iter != std::prev(s.end()); ++iter){
          std::cout << *iter << " ";
        }

        auto iter = std::prev(s.end());

        std::cout << *iter << "]";

        return os;
    }
};

template<typename T>
T add(T v) {
    return v;
}

template<typename T, typename... Args>
T add(T first, Args... args) {
    return first + add(args...);
}

template<typename T>
T sub(T v) {
    return v;
}

template<typename T, typename... Args>
T sub(T first, Args... args) {
    return first - sub(args...);
}

template<typename T>
T div(T v) {
    return v;
}

template<typename T, typename... Args>
T div(T first, Args... args) {
    return first / div(args...);
}

template<typename T>
T mul(T v) {
    return v;
}

template<typename T, typename... Args>
T mul(T first, Args... args) {
    return first * mul(args...);
}

template<typename... Args>
int println(Args... args) {
    // prints all the given arguments separated by a 'white-space' character
    ((std::cout << args << ' '), ...);
    std::cout << std::endl;
    return 0;
}

template<typename... Args>
vector<typename std::common_type<Args...>::type> vec(Args... args) {
    std::vector<typename std::common_type<Args...>::type> tmp = {args...};
    vector<typename std::common_type<Args...>::type> vector_to_return = { };
    for (auto& item : tmp) {
        vector_to_return.push_back(item);
    }
    return vector_to_return;
}

}

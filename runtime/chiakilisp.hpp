#include <iostream>
#include <vector>

namespace chiakilisp {

template<typename T>
class vector : public std::vector<T> {
public:
    friend std::ostream& operator<<(std::ostream& os, const vector<T>& self);
};

template<typename T>
std::ostream& operator<<(std::ostream& os, const vector<T>& self) {
    for (auto& item : self) os << item << ' ';
    return os;
}

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
void println(Args... args) {
    // prints all the given arguments separated by a 'white-space' character
    ((std::cout << args << ' '), ...);
    std::cout << std::endl;
}

//template<typename T, typename... Args>
//vector<T> vec(Args... args) {
//    return ((args), ...);
//}

}

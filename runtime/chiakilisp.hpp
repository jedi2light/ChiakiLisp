#include <iostream>
#include <vector>
#include <iterator>
#include <type_traits>
#include <typeinfo>
#include <functional>
#include <numeric>

#define nil NULL;

namespace chiakilisp {

// custom vector<T> class prototype

template<typename T>
class vector;

// 'str' function prototypes

// 'str' function prototypes for int

std::string _str(int v);

template<typename... Args>
std::string _str(int first, Args... args);

// 'str' function prototypes for bool

std::string _str(bool v);

template<typename... Args>
std::string _str(bool first, Args... args);

// 'str' function prototypes for char*

std::string _str(char* v);

template<typename... Args>
std::string _str(char* first, Args... args);

// 'str' function prototypes for std::string

std::string _str(std::string v);

template<typename... Args>
std::string _str(std::string first, Args... args);

// 'str' function prototypes for custom vector<T>

template<typename T>
std::string _str(vector<T> first);

template<typename... Args>
std::string _str(vector<typename std::common_type<Args...>::type> first,
                 Args... args);

// map function implementation

template<typename Predicate, typename T>
vector<T> map(const Predicate& callback, const vector<T>& sourcev) {
    vector<T> out;
    out.resize(sourcev.size());
    std::transform (begin(sourcev), end(sourcev), begin(out), callback);
    return out;
}

// filter function implementation

template<typename Predicate, typename T>
vector<T> filter(const Predicate& callback, const vector<T>& sourcev) {
    vector<T> out;
    std::remove_copy_if(begin(sourcev), end(sourcev),
                        std::back_inserter(out), std::not_fn(callback));
    return out;
}

// reduce function implementation

template<typename Predicate, typename T>
auto reduce(const Predicate& callback, const vector<T>& sourcev) {
    auto init = sourcev[0];  /* TODO: test what happens if no elements */
    auto _begin_sourcev = std::next(begin(sourcev));
    return std::accumulate(_begin_sourcev, end(sourcev), init, callback);
}

template<typename Predicate, typename T>
auto reduce(const Predicate& callback, T init, const vector<T>& sourcev){
    return std::accumulate(begin(sourcev), end(sourcev), init, callback);
}

// custom vector<T> implementation

template<typename T>
class vector : public std::vector<T> {
public:
    std::string to_str() {
        std::string to_return = "[";
        for (auto it = this->begin(); it != std::prev(this->end()); ++it) {
          to_return.append(_str(*it)).append(" ");
        }
        auto it = std::prev(this->end());
        to_return.append(_str(*it)).append("]");
        return to_return;
    }

    friend std::ostream& operator<<(std::ostream& os, const vector<T>& s) {
        std::cout << "[";

        for (auto iter = s.begin(); iter != std::prev(s.end()); ++iter) {
          std::cout << _str(*iter) << " ";
        }

        auto iter = std::prev(s.end());

        std::cout << _str(*iter) << "]";

        return os;
    }
};

// 'add' function implementations

template<typename T>
float add(T v) {
    return v;
}

template<typename T, typename... Args>
float add(T first, Args... args) {
    return first + add(args...);
}

// 'sub' function implementations

template<typename T>
float sub(T v) {
    return v;
}

template<typename T, typename... Args>
float sub(T first, Args... args) {
    return first - sub(args...);
}

// 'div' function implementations

template<typename T>
float div(T v) {
    return v;
}

template<typename T, typename... Args>
float div(T first, Args... args) {
    return first / div(args...);
}

// 'mul' function implementations

template<typename T>
float mul(T v) {
    return v;
}

template<typename T, typename... Args>
float mul(T first, Args... args) {
    return first * mul(args...);
}

// 'mod' function implementations

template<typename T>
float mod(T v) {
    return v;
}

template<typename T, typename... Args>
float mod(T first, Args... args) {
    return (int)first % (int)mod(args...);  /* explicitly cast it to int. */
}

// 'int' function implementations

// 'int' function implementation for int

int _int(int v) {
    return v;
}

// 'int' function implementation for bool

int _int(bool v) {
    return 1 ? v : 0;
}

// 'int' function implementation for char*

int _int(char* v) {
    return std::stoi(v);
}

// 'int' function implementaiton for std::string

int _int(std::string v) {
    return std::stoi(v);
}

// 'str' function implementations

// 'str' function implementations for int

std::string _str(int v) {
    return std::to_string(v);
}

template<typename... Args>
std::string _str(int first, Args... args) {
    return std::to_string(first).append(" ").append(_str(args...));
}

// 'str' function implementations for bool

std::string _str(bool v) {
    return v ? "true" : "false";
}

template<typename... Args>
std::string _str(bool first, Args... args) {
    return _str(first).append(" ").append(_str(args...));
}

// 'str' function implementations for char*

std::string _str(char* v) {
    return std::string(v);
}

template<typename... Args>
std::string _str(char* first, Args... args) {
    return std::string(first).append(" ").append(_str(args...));
}

// 'str' function implementations for std::string

std::string _str(std::string v) {
    return std::string(v);
}

template<typename... Args>
std::string _str(std::string first, Args... args) {
    return std::string(first).append(" ").append(_str(args...));
}

// 'str' function implementations for custom vector<T>

template<typename T>
std::string _str(vector<T> first) {
    return first.to_str();
}

template<typename... Args>
std::string _str(vector<typename std::common_type<Args...>::type> first,
                 Args... args) {
    return first.to_str().append(_str(args...));
}

// 'identity' function implementation

template<typename T>
T identity(T v) {
    return v;
}

// 'println' function implementation

template<typename... Args>
int println(Args... args) {
    // prints all the given arguments separated by a 'white-space' character
    ((std::cout << args << ' '), ...);
    std::cout << std::endl;
    return 0;
}

// 'vec' function implementation

template<typename... Args>
vector<typename std::common_type<Args...>::type> vec(Args... args) {
    std::vector<typename std::common_type<Args...>::type> tmp = {args...};
    vector<typename std::common_type<Args...>::type> vector_to_return = { };
    for (auto& item : tmp) {
        vector_to_return.push_back(item);
    }
    return vector_to_return;
}

// 'get' function implementations

template<typename T>
T get(vector<T>& v, int idx, T def) {
    return idx < v.size() ? v[idx] : def;
}

template<typename T>
T get(vector<T>& v, int idx) {
    return get(v, idx, NULL);
}

}

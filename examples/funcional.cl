;; this example shows functional programming style using
;; famous 'map', 'filter', and 'reduce' functions

;; also, this example shows a little ChiakiLisp' benefit:
;; expressions arranging with first/last threading macro 

;; you can run this example via both eval, and cxx modes

;; eval-mode requirements: Python 3 interpreter in $PATH

;; to run this example in eval-mode run:
;; $ ./chiakilang examples/functional.cl

;; cxx-mode requirements: Clang or any compiler in $PATH
;; you also need to build "ChiakiLisp C++ Runtime" using
;; CMake. Run 'make cxx-runtime' if you are on GNU/Linux

;; to run this example in cxx-mode run:
;; $ ./chiakilangc examples/functional.cl

(defn ^t:bool even? (^t:int x)
 (if (= (mod x 2) 0) true false))

(defn ^t:int inc (^t:int x)
 (+ x 1))

(defn ^t:int add (^t:int acc ^t:int cur)
 (+ acc cur))

(def foo [1 2 3])

(prn "source vector =>" foo)

(prn "map, filter, reduce result =>" (->> foo
                                          (map inc)
                                          (filter even?)
                                          (reduce add)))

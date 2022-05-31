;; this program prints recursivelly calculated factorial

;; you can run this example via both eval, and cxx modes

;; eval-mode requirements: Python 3 interpreter in $PATH

;; to run this example in eval-mode run:
;; $ ./chiakilang examples/factorial.cl

;; cxx-mode requirements: Clang or any compiler in $PATH
;; you also need to build "ChiakiLisp C++ Runtime" using
;; CMake. Run 'make cxx-runtime' if you are on GNU/Linux

;; to run this example in cxx-mode run:
;; $ ./chiakilangc examples/factorial.cl

;; in eval-mode '^float' property wil be ignored, but in
;; cxx-mode we can assign function-returning-type. Also,
;; we can assign a parameter type the same way, although
;; it's not such a requirement (at least in _this_ case)

(defn ^float fac (n)
 (if (= n 1)
  n
  (* n (fac (- n 1)))))

(prn (fac 4))
(prn (fac 164)) ;; in eval-mode, it's max possible value
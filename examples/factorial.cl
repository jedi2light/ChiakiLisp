;;; this program prints recursively calculated factorial

;;; you can run this example via both AST, and cxx modes

;;; ast-mode requirements: Python 3 interpreter in $PATH

;; to run this example in ast-mode:
;;                  $ ./chiakilang examples/factorial.cl

;; cxx-mode requirements: Clang or any compiler in $PATH
;; you also need to build "ChiakiLisp C++ Runtime" using
;; CMake. Run 'make cxx-runtime' if you are on GNU/Linux

;; to run this example in cxx-mode:
;;                  $ ./chiakilang \
;;                      --cxx-mode examples/factorial.cl
;;                  $ ./chiakilang \
;;                      --bin-mode examples/factorial.cl
;;                  $ ./factorial  # will run the binary

(defn ^t:int fac (n)
 (if (= n 1)
  n
  (* n (fac (- n 1)))))

(prn (fac 4))
(prn (fac 20)) ;; max possible value for both C++/Python
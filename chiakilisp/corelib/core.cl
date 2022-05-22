;; a ChiakiLisp core library
;; general purpose functions
(defn identity (x) x)
;; collection related functions
(defn count (x) (.__len__ x))
;; numbers related functions
(defn even? (x) (= (mod x 2) 0))
(defn positive? (x) (> x 0))
(defn inc (x) (+ x 1))
(defn dec (x) (- x 1))
;; all data types related functions
(defn nil? (x) (= x nil))
(defn number? (x) (isinstance x int))
(defn string? (x) (isinstance x str))
(defn boolean? (x) (isinstance x bool))
(defn = (first second) (.__eq__ first second))
(defn < (first second) (.__lt__ first second))
(defn > (first second) (.__gt__ first second))
(defn <= (first second) (.__le__ first second))
(defn >= (first second) (.__ge__ first second))
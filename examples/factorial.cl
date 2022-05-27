(defn fac (n)
 (if (= n 1)
  n
  (* n (fac (- n 1)))))

(prn (fac 4)) ;; _=> 24
(prn (fac 165)) ; limit

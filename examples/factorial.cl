(defn fac (n)
 (if (= n 1)
  n
  (* n (fac (- n 1)))))

(fac 4) ; will print 24
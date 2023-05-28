(import random)

(defn bubble-sort* (lst)
 (let ((x y) lst
       tail  (get lst 2..))
  (if (or (nil? x) (nil? y))
   lst
   (if (> x y)
    (cons y (cons x (bubble-sort* tail)))
    (cons x (bubble-sort* (rest lst)))))))

(defn bubble-sort (lst)
 (let (bubbled (bubble-sort* lst))
  (if (= lst bubbled) lst (bubble-sort bubbled))))

(def source (->> 10 range (map #(random/randint % (+ 5 %))) list))

(prn "Source list (randomly populated, length of the 10 numbers) =>", source)
(prn "Result list (sorted using recursive bubble sort algorithm) =>", (bubble-sort source))
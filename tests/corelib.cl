;; this file contains tests for the ChiakiLisp core library, should be updated alongside corelibrary

(def identity-tests [{:run "(identity 10)" :expected 10}
                     {:run "(identity \"Hello\")" :expected "Hello"}])

(def constantly-tests [{:run "(let (function (constantly 10)) (function))" :expected 10}
                        {:run "(let (function (constantly \"Hello\")) (function))" :expected "Hello"}])

(def inc-tests []) ;; todo: implement (core/inc) tests
(def dec-tests []) ;; todo: implement (core/dev) tests
(def odd?-tests []) ;; todo: implement (core/odd?) tests
(def even?-tests []) ;; todo: implement (core/even?) tests
(def zero?-tests [])) ;; todo: implement (core/zero?) tests
(def positive?-tests []) ;; todo: implement (core/positive? tests)

(def all-tests [identity-tests
                constantly-tests
                inc-tests
                dec-tests
                odd?-tests
                even?-tests
                zero?-tests
                positive?-tests])

(for (specific-tests all-tests)
 (for (specific-test specific-tests)
  (let ({run
         expected}     specific-test
        test-result    (-> run eval list first)
        successful?    (= test-result expected))
   (prn run (if successful? "PASSED" (+ "FAILED: expected: " (str expected) " got: " (str test-result)))))))
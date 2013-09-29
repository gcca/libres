(ns js.core)

;; // ==ClosureCompiler==
;; // @compilation_level WHITESPACE_ONLY
;; // @output_file_name default.js
;; // ==/ClosureCompiler==

(defn tres [a b c]
  (if (or (= a 1) (= 1 b))
    (+ a b)
    (- b c)
    )
  )

(js/console.log "ClojureScript!")

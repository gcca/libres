(defproject js "0.1.0-SNAPSHOT"
  :description "gcca cljs"
  :dependencies [[org.clojure/clojure "1.5.1"]
                 [org.clojure/clojurescript "0.0-1859"
                  :exclusions [org.apache.ant/ant]]
                 ]
  :plugins [[lein-cljsbuild "0.3.4-SNAPSHOT"]
            ]
  :cljsbuild {
    :builds [{:source-paths ["src"]
              :compiler {:output-to "js/main.js"
                         :optimizations :whitespace
                         :pretty-print true}}]}
  )

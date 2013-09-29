(defproject cljgae "1.0.0-SNAPSHOT"
  :description "FIXME: write description"
  :dependencies [[org.clojure/clojure "1.3.0"]
                 [compojure "1.1.5"]
                 [appengine "0.4.3-SNAPSHOT"]]
  :dev-dependencies [[lein-swank "1.4.5"]]
  :compile-path "war/WEB-INF/classes"
  :library-path "war/WEB-INF/lib")

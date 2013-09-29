(ns cljgae.core
  (:gen-class :extends javax.servlet.http.HttpServlet)
  (:use
    compojure.core
    [ring.util.servlet :only [defservice]])
  (:require [compojure.route :as route]))

(defroutes cms-public
  (GET "/" []
       "<html><title>GAE CMS</title><body><h1>Hello World!</h1></body>"))

(defroutes cms
  cms-public
  (route/not-found "Page not found")) ; 404 error page

(defservice cms)

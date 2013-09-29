import sbtappengine.Plugin.{AppengineKeys => gae}

name := "sample"

scalaVersion := "2.9.2"

libraryDependencies ++= Seq(
  "net.databinder" %% "unfiltered-filter" % "0.6.4",
  "javax.servlet" % "servlet-api" % "2.5" % "provided",
  "org.mortbay.jetty" % "jetty" % "6.1.22" % "container"
)

appengineSettings

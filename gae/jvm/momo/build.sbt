name := "momo"

// scalaVersion := "2.10"

libraryDependencies ++= Seq(
  "javax.servlet" % "servlet-api" % "2.5" % "provided",
  "javax.jdo" % "jdo-api" % "3.0.1"
)

classDirectory in Compile <<= baseDirectory { _ / "war/WEB-INF/classes" }

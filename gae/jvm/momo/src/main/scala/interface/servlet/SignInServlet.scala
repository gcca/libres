package interface.servlet

import javax.servlet.http.{
  HttpServlet,
  HttpServletRequest,
  HttpServletResponse }
import javax.jdo.Query
import domain.PMF
import domain.model.User

class SignInServlet extends HttpServlet {
  override def doPost(req: HttpServletRequest, resp: HttpServletResponse) = {
    val pm = PMF.get().getPersistenceManager()

    val username = req.getParameter("username")
    val password = req.getParameter("password")

    val q = pm.newQuery(classOf[User])
      q.setFilter("username == usernameParam && password == passwordParam")
    q.declareParameters("String usernameParam, String passwordParam")

    val isAuth = try {
      val res = q.execute(username, password).asInstanceOf[java.util.List[User]]
      val users = List(res.toArray: _*) map (_.asInstanceOf[User])
      users.length > 0
    } catch {
      case _: Exception => false
    } finally {
      q.closeAll()
    }

    if (isAuth) {
      resp.sendRedirect("/dashboard.jsp")
    } else {
      resp.setContentType("text/plain")
      resp.getWriter().println("No Logueado")
    }
  }
}
